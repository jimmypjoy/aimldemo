import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from llm_response_chat_rag import initialize_db, response_from_llm
import os

st.title("RAG Chatbot")

# Highlight the best matching chunk in the PDF and save it to a file
def highlight_chunk_and_save(pdf_path, output_path, text_to_highlight, chunk_size=200):
    """Highlight the best matching chunk in the PDF and save it to a file."""
    doc = fitz.open(pdf_path)
    highest_similarity = 0
    best_page_number = None  # To store the page number of the best match
    best_match_rects = None

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()

        # Split page text into smaller chunks
        page_chunks = [page_text[i:i + chunk_size] for i in range(0, len(page_text), chunk_size)]

        # Perform text similarity search using TF-IDF and cosine similarity
        vectorizer = TfidfVectorizer().fit_transform([text_to_highlight] + page_chunks)
        similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

        # Find the chunk with the highest similarity score
        max_sim_index = similarities.argmax()
        max_sim = similarities[max_sim_index]

        # Update the best match if this page has a higher similarity score
        if max_sim > highest_similarity:
            highest_similarity = max_sim
            best_page_number = page_num  # Store the page number
            best_chunk = page_chunks[max_sim_index]
            best_match_rects = page.search_for(best_chunk)

    # Highlight the best match
    if best_page_number is not None and best_match_rects:
        best_page = doc[best_page_number]
        for rect in best_match_rects:
            best_page.add_highlight_annot(rect)
        print(f"[INFO] Added highlights on page {best_page_number + 1} for chunk: {text_to_highlight[:50]}...")
    else:
        print(f"[WARNING] No highlights added for: {text_to_highlight}")

    # Save the PDF to the specified output path
    doc.save(output_path, garbage=4)  # Ensure garbage collection and compression
    doc.close()

    print(f"[INFO] Highlighted PDF saved to: {output_path}")

    return best_page_number  # Return the page number

# Paths
pdf_path = "C:\\gitworkspace\\aimldemo\\jupyterworkapce\\11 genAI\\doc_inputs\\Form_2287.pdf"
output_folder = os.path.dirname(__file__)
highlighted_pdf_path = os.path.join(output_folder, "highlighted_output.pdf")

# Button to download the highlighted PDF
if os.path.exists(highlighted_pdf_path):
    with open(highlighted_pdf_path, "rb") as file:
        st.download_button(
            label="Response Document Traceback",
            data=file,
            file_name="highlighted_output.pdf",
            mime="application/pdf",
            key="download-button"
        )

# Initialize vector DB
if "db_initialized" not in st.session_state:
    db_path = "chroma_db"
    initialize_db(pdf_path, db_path)
    st.session_state.db_initialized = True

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
st.markdown("### Chat Conversation")

# Display conversation history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat Input
user_input = st.chat_input("Ask a question about the document.")

if user_input is not None and user_input.strip():
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        # Get response from backend
        top_chunk, metadata, full_response = response_from_llm(user_input, st.session_state.chat_history)

        # Highlight the best matching chunk dynamically and save to file system
        best_page_number = highlight_chunk_and_save(pdf_path, highlighted_pdf_path, top_chunk)
        print(f"[INFO] Updated PDF saved with highlights to: {highlighted_pdf_path}")

        # Create the URL with the page number as a query parameter
        pdf_viewer_url = f"http://localhost:8502/?page={best_page_number}"  # Adding 1 to match typical page numbering

        # Display the "Test Traceback" button
        st.markdown(
            f'<a href="{pdf_viewer_url}" target="_blank"><button>Test Traceback</button></a>',
            unsafe_allow_html=True
        )

        # Display response
        placeholder.markdown(full_response)
        st.session_state.chat_history.append(AIMessage(content=full_response))
