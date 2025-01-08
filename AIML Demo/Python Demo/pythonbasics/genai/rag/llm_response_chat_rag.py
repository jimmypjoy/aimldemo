import os
import shutil
import json
import requests
import fitz
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer, CrossEncoder, util
from chromadb.config import Settings

nltk.download('punkt')

# Initialize Cross-Encoder for ranking
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Initialize Sentence Transformer for cosine similarity
similarity_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


class HuggingFaceEmbeddings:
    """Custom wrapper for Hugging Face SentenceTransformer embeddings."""
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        """Generate embeddings for a list of documents."""
        return self.embedding_model.encode(texts, convert_to_tensor=False).tolist()
    
    def embed_query(self, text):
        """Generate embedding for a single query."""
        return self.embedding_model.encode(text, convert_to_tensor=False).tolist()


def initialize_db(pdf_dir, db_path):
    """Process all PDF files in the directory, chunk them, and store in the Chroma vector database with metadata."""
    if os.path.exists(db_path):
        print(f"[INFO] Deleting existing Chroma database at {db_path} to avoid conflicts.")
        shutil.rmtree(db_path, ignore_errors=True)

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)

    # Process each PDF file in the directory
    for file_name in os.listdir(pdf_dir):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file_name)
            text_chunks_with_metadata = extract_chunks_with_coordinates(pdf_path, file_name)
            chunk_texts = [item["text"] for item in text_chunks_with_metadata]
            metadata = [
                {
                    "file_name": file_name,
                    "page": item["page"],
                    "coordinates": json.dumps(item["coordinates"])
                }
                for item in text_chunks_with_metadata
            ]

            vector_db.add_texts(chunk_texts, metadatas=metadata)

    vector_db.persist()
    print("[INFO] Vector database initialized with all PDF files.")


def extract_chunks_with_coordinates(pdf_path, file_name, chunk_size=500, chunk_overlap=50):
    """Extract chunks from the PDF along with their coordinates (bounding boxes) and file name."""
    doc = fitz.open(pdf_path)
    chunks_with_metadata = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text("blocks")
        full_text = " ".join(block[4] for block in page_text)

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        text_chunks = splitter.split_text(full_text)

        for chunk in text_chunks:
            coordinates = []
            search_results = page.search_for(chunk)
            for rect in search_results:
                coordinates.append((rect.x0, rect.y0, rect.x1, rect.y1))

            chunks_with_metadata.append({
                "text": chunk,
                "file_name": file_name,
                "page": page_num,
                "coordinates": coordinates
            })

    return chunks_with_metadata


def response_from_llm(user_question, chat_history):
    """Retrieve, rank, and send the best context to the LLM based on metadata filtering."""
    db_path = "chroma_db"

    print("&" * 50)
    print("Inside response_from_llm")

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)

    # Step 1: Split the user query into metadata and actual query using the external service
    print(f"User question: {user_question}")
    
    split_url = "http://127.0.0.1:5000/split_query"
    response = requests.post(split_url, json={"question": user_question})
    
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    response_data = response.json()
    print(f"Response data: {response_data}")

    # Extract metadata and actual query
    raw_metadata = response_data.get("metadata", {})
    actual_query = response_data.get("query", "").strip()

    print(f"Raw metadata: {raw_metadata}")
    print(f"Actual query: {actual_query}")

    # Step 2: Perform vector similarity search with metadata filtering
    result_sets = []
    for key, value in raw_metadata.items():
        metadata_filter = {key: {"$eq": value}}
        print(f"Performing search with filter: {metadata_filter}")
        
        results = vector_db.similarity_search(actual_query, 5, filter=metadata_filter)
        
        if results:
            # Convert results to a set of tuples (page_content, metadata) for intersection
            result_set = set((doc.page_content, json.dumps(doc.metadata)) for doc in results)
            result_sets.append(result_set)
            print(f"Results for {key}: {result_set}")
        else:
            print(f"No results for filter: {metadata_filter}")
    
    # Check if any result set is empty before intersecting
    if not result_sets:
        print("[INFO] No matching documents found.")
        return "[INFO] No matching documents found.", {}, ""

    # Find intersection of non-empty result sets
    intersected_results = set.intersection(*result_sets) if result_sets else set()
    
    print(f"Final intersected results: {intersected_results}")

    if not intersected_results:
        return "[INFO] No matching documents found.", {}, ""

    # Extract the top chunk and its metadata
    top_chunk_content, top_metadata_str = list(intersected_results)[0]  # Get the first result
    top_chunk = top_chunk_content
    metadata = json.loads(top_metadata_str)  # Deserialize metadata

    # Debugging print to ensure 'file_name' is present in metadata
    print(f"Retrieved metadata: {metadata}")

    payload = {
        "chathistory": [msg.content for msg in chat_history],
        "context": top_chunk,
        "question": actual_query
    }

    # Print the payload before sending it to the Flask service
    print(f"Payload sent to LLM service: {payload}")

    response = requests.post("http://127.0.0.1:5000/", json=payload)
    response.raise_for_status()
    full_response = response.json().get("answer", "No answer provided.")

    return top_chunk, metadata, full_response

def get_sentences_similarity(pdf_path, page_num, chunk_coordinates, llm_response, threshold):
    """Compare cosine similarity of each sentence in the chunk with the LLM response and return high-similarity sentences."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)

    # Extract the chunk text using the provided coordinates
    chunk_text = " ".join(page.get_textbox(fitz.Rect(*coord)) for coord in chunk_coordinates)

    # Tokenize the chunk into sentences
    sentences = nltk.sent_tokenize(chunk_text)

    # Compute embeddings for the LLM response and sentences
    llm_response_embedding = similarity_model.encode(llm_response, convert_to_tensor=True)
    sentence_embeddings = similarity_model.encode(sentences, convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.cos_sim(llm_response_embedding, sentence_embeddings)[0].tolist()

    # Pair sentences with their similarity scores
    sentences_with_scores = list(zip(sentences, similarities))

    # Find high-similarity sentences and their coordinates
    high_similarity_sentences = []
    for sentence, score in sentences_with_scores:
        if score >= threshold:
            search_results = page.search_for(sentence)
            if search_results:  # Ensure search_results is not empty
                high_similarity_sentences.append(fitz.Rect(*search_results[0]))

    return high_similarity_sentences
