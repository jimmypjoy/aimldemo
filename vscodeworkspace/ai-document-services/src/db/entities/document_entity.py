import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "doc_ai"}

    document_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    original_file_name: Mapped[Optional[str]] = mapped_column(String(500))
    document_type: Mapped[Optional[str]] = mapped_column(String(100))
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    page_count: Mapped[Optional[int]] = mapped_column(Integer)
    is_scanned: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    source_system: Mapped[Optional[str]] = mapped_column(String(100))
    storage_uri: Mapped[Optional[str]] = mapped_column(Text)
    document_hash: Mapped[Optional[str]] = mapped_column(String(256), unique=True)
    ingestion_status: Mapped[str] = mapped_column(String(50), default="PENDING")
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
