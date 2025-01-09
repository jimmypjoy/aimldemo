import streamlit as st
import fitz  # PyMuPDF

def display_page(pdf_path, page_number):
    """Extract and display a specific page from the PDF."""
    try:
        doc = fitz.open(pdf_path)
        if page_number < 0 or page_number >= len(doc):
            st.error("Invalid page number.")
            return
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        image_data = pix.tobytes("png")
        st.image(image_data, caption=f"Page {page_number + 1}", use_column_width=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")


st.title("PDF Viewer")

# Retrieve query parameters
query_params = st.query_params
page_number = int(query_params.get("page", [0])[0])

pdf_path = "C:/gitworkspace/aimldemo/AIML Demo/Python Demo/pythonbasics/genai/chatbot_rag/highlighted_output.pdf"

display_page(pdf_path, page_number)
