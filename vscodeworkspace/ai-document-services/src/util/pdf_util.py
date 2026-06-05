import io
import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

_MIN_TEXT_PER_PAGE = 50  # chars — below this threshold the page is treated as scanned


def extract_pdf_text(file_path: Path) -> tuple[list[tuple[int, str]], bool]:
    """
    Extract text from a PDF. Detects scanned pages and falls back to OCR.

    Returns:
        (pages, is_scanned) where pages is a list of (page_number, text) tuples.
        Page numbers are 1-based.
    """
    doc = fitz.open(str(file_path))
    pages_raw: list[tuple[int, str]] = []
    total_chars = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text()
        pages_raw.append((page_index + 1, text))
        total_chars += len(text.strip())

    page_count = len(pages_raw)
    avg_chars = total_chars / page_count if page_count else 0
    is_scanned = avg_chars < _MIN_TEXT_PER_PAGE

    if is_scanned:
        logger.info("Scanned PDF detected | file=%s avg_chars_per_page=%.1f — switching to OCR",
                    file_path.name, avg_chars)
        pages = _ocr_pages(doc)
    else:
        pages = pages_raw

    doc.close()
    logger.info("PDF extraction complete | file=%s pages=%d scanned=%s",
                file_path.name, page_count, is_scanned)
    return pages, is_scanned


def _ocr_pages(doc: fitz.Document) -> list[tuple[int, str]]:
    """Render each page to an image and run pytesseract OCR."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "pytesseract and Pillow are required for OCR. "
            "Install with: pip install pytesseract Pillow"
        ) from exc

    pages: list[tuple[int, str]] = []
    scale_matrix = fitz.Matrix(2.0, 2.0)  # 2x scale improves OCR accuracy

    for page_index in range(len(doc)):
        page = doc[page_index]
        pixmap = page.get_pixmap(matrix=scale_matrix)
        img = Image.open(io.BytesIO(pixmap.tobytes("png")))
        text = pytesseract.image_to_string(img)
        pages.append((page_index + 1, text))
        logger.debug("OCR page %d | chars=%d", page_index + 1, len(text))

    return pages
