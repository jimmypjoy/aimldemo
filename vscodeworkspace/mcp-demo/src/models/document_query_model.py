import uuid
from typing import List, Optional

from pydantic import BaseModel


class DocumentQueryRequest(BaseModel):
    query: str
    file_name: Optional[str] = None
    top_k: int = 5
    llm_model: Optional[str] = "gemini-3.1-pro-preview"


class ChunkResult(BaseModel):
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    file_name: str
    chunk_sequence: int
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    chunk_text: str
    similarity_score: float


class DocumentQueryResponse(BaseModel):
    query: str
    file_name: Optional[str] = None
    results: List[ChunkResult]
    total_results: int
    llm_answer: Optional[str] = None
    llm_model: Optional[str] = None
