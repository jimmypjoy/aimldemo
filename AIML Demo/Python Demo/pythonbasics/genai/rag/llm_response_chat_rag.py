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

# Download NLTK tokenizer



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


def initialize_db(pdf_path, db_path):
    """Process the PDF, chunk it, and store it in the Chroma vector database with chunk coordinates."""
    if os.path.exists(db_path):
        print(f"[INFO] Deleting existing Chroma database at {db_path} to avoid conflicts.")
        shutil.rmtree(db_path, ignore_errors=True)

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)

    text_chunks_with_metadata = extract_chunks_with_coordinates(pdf_path)
    chunk_texts = [item["text"] for item in text_chunks_with_metadata]
    metadata = [{"page": item["page"], "coordinates": json.dumps(item["coordinates"])} for item in text_chunks_with_metadata]

    vector_db.add_texts(chunk_texts, metadatas=metadata)
    vector_db.persist()


def extract_chunks_with_coordinates(pdf_path, chunk_size=500, chunk_overlap=50):
    """Extract chunks from the PDF along with their coordinates (bounding boxes)."""
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
                "page": page_num,
                "coordinates": coordinates
            })

    return chunks_with_metadata


def response_from_llm(user_question, chat_history):
    """Retrieve, rank, and send the best context to the LLM."""
    db_path = "chroma_db"

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)

    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)

    # Step 1: Retrieve top 5 chunks from vector database based on initial similarity
    top_chunks_with_scores = vector_db.similarity_search_with_score(user_question, k=2)

    # Print the initial top 5 chunks with their similarity scores
    print("\n[INFO] Initial top 5 chunks retrieved from vector DB:")
    for i, (chunk, score) in enumerate(top_chunks_with_scores, 1):
        print("#" * 50)
        print(f"Chunk {i} (Score: {score:.4f}): {chunk.page_content}...")

    # Extract chunk texts for cross-encoding
    top_chunks = [chunk.page_content for chunk, _ in top_chunks_with_scores]

    # Step 2: Cross-encode the chunks and re-rank based on cross-encoder scores
    query_chunk_pairs = [(user_question, chunk) for chunk in top_chunks]
    cross_encoded_scores = cross_encoder.predict(query_chunk_pairs)

    # Pair chunks with their cross-encoder scores and sort them in descending order
    ranked_chunks_with_scores = sorted(
        zip(top_chunks_with_scores, cross_encoded_scores),
        key=lambda x: x[1],  # Sort by score (descending)
        reverse=True
    )

    # Use the top-ranked chunk after re-ranking
    top_chunk, score = ranked_chunks_with_scores[0][0]
    metadata = top_chunk.metadata
    metadata["coordinates"] = json.loads(metadata["coordinates"])  # Deserialize coordinates

    payload = {
        "chathistory": [msg.content for msg in chat_history],
        "context": top_chunk.page_content,
        "question": user_question
    }

    response = requests.post("http://127.0.0.1:5000/", json=payload)
    response.raise_for_status()
    full_response = response.json().get("answer", "No answer provided.")

    return top_chunk.page_content, metadata, full_response

def get_sentences_similarity(pdf_path, page_num, chunk_coordinates, llm_response, threshold):
    """Compare cosine similarity of each sentence in the chunk with the LLM response and return high-similarity sentences."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    
    print("*" * 50)
    print("Inside get_sentences_similarity:")

    # Extract the chunk text using the provided coordinates
    chunk_text = " ".join(page.get_textbox(fitz.Rect(*coord)) for coord in chunk_coordinates)
    print("chunk_text:", chunk_text)
    print("llm_response: "+llm_response)

    # Tokenize the chunk into sentences
    sentences = nltk.sent_tokenize(chunk_text)

    # Compute embeddings for the LLM response and sentences
    llm_response_embedding = similarity_model.encode(llm_response, convert_to_tensor=True)
    sentence_embeddings = similarity_model.encode(sentences, convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.cos_sim(llm_response_embedding, sentence_embeddings)[0].tolist()

    # Pair sentences with their similarity scores
    sentences_with_scores = list(zip(sentences, similarities))

    # Sort sentences by similarity score in descending order
    sorted_sentences_with_scores = sorted(sentences_with_scores, key=lambda x: x[1], reverse=True)

    # Print sorted sentences with similarity scores
    print("\n[INFO] Sentences sorted by cosine similarity:")
    for sentence, score in sorted_sentences_with_scores:
        print(f"Score: {score:.4f}, Sentence: {sentence}")

    # Find high-similarity sentences and their coordinates
    high_similarity_sentences = []
    for sentence, score in sorted_sentences_with_scores:
        if score >= threshold:
            search_results = page.search_for(sentence)
            if search_results:  # Ensure search_results is not empty
                high_similarity_sentences.append(fitz.Rect(*search_results[0]))

    return high_similarity_sentences
