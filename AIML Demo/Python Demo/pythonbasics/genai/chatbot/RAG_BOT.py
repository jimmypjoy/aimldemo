from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGBot:
    def __init__(self, pdf_path):
        """Initialize the RAG Bot with a PDF file path"""
        self.pdf_path = pdf_path
        self.llm = OpenAI(temperature=0)
        self.vector_store = None
        self.setup_knowledge_base()

    def setup_knowledge_base(self):
        """Process the PDF and create a searchable knowledge base"""
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_documents(texts, embeddings)

    def get_response(self, query: str) -> str:
        """Get response for a query using the RAG system"""
        # Custom prompt to ensure answers come from the PDF
        custom_prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say "I don't have enough information to answer this question."
        Please provide specific references from the context when possible.

        Context: {context}

        Question: {question}

        Answer:"""

        PROMPT = PromptTemplate(
            template=custom_prompt_template,
            input_variables=["context", "question"]
        )

        # Create chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        # Get response
        result = qa_chain({"query": query})
        
        return result["result"]

def main():
    # Example usage
    pdf_path = "path/to/your/document.pdf"
    
    try:
        rag_bot = RAGBot(pdf_path)
        
        # Example queries
        queries = [
            "What is the main topic of the document?",
            "Can you summarize the key points?"
        ]
        
        for query in queries:
            print(f"\nQuestion: {query}")
            response = rag_bot.get_response(query)
            print(f"Answer: {response}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
