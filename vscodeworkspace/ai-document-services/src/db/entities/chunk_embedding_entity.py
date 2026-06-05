import uuid
from datetime import datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"
    __table_args__ = {"schema": "doc_ai"}

    embedding_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chunk_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doc_ai.document_chunks.chunk_id"), nullable=False
    )
    embedding_type: Mapped[Optional[str]] = mapped_column(String(50))
    embedding_model: Mapped[Optional[str]] = mapped_column(String(100))
    embedding: Mapped[Optional[list]] = mapped_column(Vector(1536))
    created_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
