import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ProcessingRun(Base):
    __tablename__ = "processing_runs"
    __table_args__ = {"schema": "doc_ai"}

    run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("doc_ai.documents.document_id"), nullable=False
    )
    run_type: Mapped[Optional[str]] = mapped_column(String(100))
    agent_name: Mapped[Optional[str]] = mapped_column(String(200))
    llm_model: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    start_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    run_config_json: Mapped[Optional[dict]] = mapped_column(JSONB)
