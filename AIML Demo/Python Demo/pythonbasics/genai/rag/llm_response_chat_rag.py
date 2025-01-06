import os
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma  # Updated import
from sentence_transformers import SentenceTransformer, CrossEncoder
from chromadb.config import Settings
import requests
import fitz

# Initialize Cross-Encoder for ranking
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


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
    """Process the PDF, chunk it, and store it in the Chroma vector database."""
    if os.path.exists(db_path):
        print(f"[INFO] Deleting existing Chroma database at {db_path} to avoid conflicts.")
        shutil.rmtree(db_path, ignore_errors=True)

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)

    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)
    text = process_pdf(pdf_path)
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_text(text)
    vector_db.add_texts(chunks)
    vector_db.persist()


def process_pdf(pdf_path):
    """Extract text from the PDF."""
    with fitz.open(pdf_path) as doc:
        return " ".join(page.get_text() for page in doc)


def response_from_llm(user_question, chat_history):
    """Retrieve, rank, and send the best context to the LLM."""
    db_path = "chroma_db"

    embeddings = HuggingFaceEmbeddings()
    chroma_settings = Settings(persist_directory=db_path, anonymized_telemetry=False)

    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings, client_settings=chroma_settings)
    top_chunks = vector_db.similarity_search_with_score(user_question, k=5)
    top_chunk = top_chunks[0][0].page_content

    payload = {
        "chathistory": [msg.content for msg in chat_history],
        "context": top_chunk,
        "question": user_question
    }

    response = requests.post("http://127.0.0.1:5000/", json=payload)
    response.raise_for_status()
    full_response = response.json().get("answer", "No answer provided.")

    return top_chunk, {}, full_response
