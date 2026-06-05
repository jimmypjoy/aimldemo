import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IngestResponse(BaseModel):
    document_id: uuid.UUID
    file_name: str
    ingestion_status: str
    page_count: Optional[int] = None
    chunk_count: Optional[int] = None
    is_scanned: bool = False
    message: str
    success: bool


class DocumentListItem(BaseModel):
    document_id: uuid.UUID
    file_name: str
    ingestion_status: str
    page_count: Optional[int] = None
    is_scanned: bool = False
    created_timestamp: Optional[datetime] = None


class DeleteResponse(BaseModel):
    file_name: str
    chunks_deleted: int
    embeddings_deleted: int
    processing_runs_deleted: int
    message: str
    success: bool
