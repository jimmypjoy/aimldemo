import fitz  # PyMuPDF
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from llm_response_chat_rag import initialize_db, response_from_llm, get_sentences_similarity
import os

# Configurable cosine similarity threshold
COSINE_SIMILARITY_THRESHOLD = 0.4

st.title("RAG Chatbot")

def highlight_chunk_with_coordinates(pdf_path, output_path, page_num, coordinates, sentences_with_high_similarity):
    """Highlight the chunk in yellow and high-similarity sentences in green."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)

    # Highlight the entire chunk in yellow
    for coord in coordinates:
        rect = fitz.Rect(*coord)
        page.add_highlight_annot(rect)

    # Highlight high-similarity sentences in green
    for sentence_coords in sentences_with_high_similarity:
        rect = fitz.Rect(*sentence_coords)
        highlight = page.add_highlight_annot(rect)
        highlight.set_colors(stroke=(0, 1, 0))  # Green color
        highlight.update()

    doc.save(output_path, garbage=4)
    doc.close()


# Paths
pdf_dir = "C:\\gitworkspace\\aimldemo\\jupyterworkapce\\11 genAI\\doc_inputs"
output_folder = os.path.dirname(__file__)
highlighted_pdf_path = os.path.join(output_folder, "highlighted_output.pdf")

# Initialize vector DB
if "db_initialized" not in st.session_state:
    db_path = "chroma_db"
    initialize_db(pdf_dir, db_path)
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

        # Get high-similarity sentences within the chunk
        pdf_path = os.path.join(pdf_dir, metadata["file_name"])
        sentences_with_high_similarity = get_sentences_similarity(
            pdf_path, metadata["page"], metadata["coordinates"], full_response, COSINE_SIMILARITY_THRESHOLD
        )

        # Highlight the best matching chunk dynamically and save to file system
        highlight_chunk_with_coordinates(
            pdf_path, highlighted_pdf_path, metadata["page"], metadata["coordinates"], sentences_with_high_similarity
        )
        print(f"[INFO] Updated PDF saved with highlights to: {highlighted_pdf_path}")

        # Create the URL with the page number as a query parameter
        pdf_viewer_url = f"http://localhost:8502/?page={metadata['page']}"

        # Display the "Test Traceback" button
        st.markdown(
            f'<a href="{pdf_viewer_url}" target="_blank"><button>Test Traceback</button></a>',
            unsafe_allow_html=True
        )

        # Display response
        placeholder.markdown(full_response)
        st.session_state.chat_history.append(AIMessage(content=full_response))
