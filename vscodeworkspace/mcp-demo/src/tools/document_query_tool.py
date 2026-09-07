from models.document_query_model import DocumentQueryRequest
from services.document_query_service import DocumentQueryService

_service = DocumentQueryService()


async def query_document(
    query: str,
    file_name: str = "",
    top_k: int = 5,
    llm_model: str = "gemini-3.1-pro-preview",
) -> str:
    """
    Search ingested PDF documents for chunks relevant to a query and return an
    LLM-generated answer grounded in those chunks, with page-level citations.

    Args:
        query: The search phrase or question to look up in the document store.
        file_name: Optional. Scope the search to a specific ingested PDF file name.
                   Pass an empty string to search across all ingested documents.
        top_k: Number of relevant chunks to retrieve (default 5).
        llm_model: Chat model to use for generating the answer
                   (default gemini-3.1-pro-preview).

    Returns:
        JSON string containing the retrieved chunks (text, page, file name,
        similarity score) and the LLM-generated answer with citations.
    """
    request = DocumentQueryRequest(
        query=query,
        file_name=file_name or None,
        top_k=top_k,
        llm_model=llm_model or None,
    )
    response = await _service.query(request)
    return response.model_dump_json(indent=2)
