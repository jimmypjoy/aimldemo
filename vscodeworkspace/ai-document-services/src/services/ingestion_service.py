import hashlib
import logging
import uuid
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import get_settings
from db.entities.chunk_embedding_entity import ChunkEmbedding
from db.entities.document_chunk_entity import DocumentChunk
from db.entities.document_entity import Document
from db.entities.processing_run_entity import ProcessingRun
from models.document.ingest_request import IngestRequest
from models.document.ingest_response import IngestResponse
from util.embedding_util import get_embeddings_batch
from util.pdf_util import extract_pdf_text

logger = logging.getLogger(__name__)
settings = get_settings()


def _compute_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]


class IngestionService:

    async def ingest_document(
        self, request: IngestRequest, session: AsyncSession
    ) -> IngestResponse:
        logger.info("IngestionService.ingest_document ENTRY | file_name=%s", request.file_name)

        file_path = Path(settings.documents_base_path) / request.file_name
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        doc_hash = _compute_file_hash(file_path)

        # Return early if already successfully ingested
        existing_result = await session.execute(
            select(Document).where(Document.document_hash == doc_hash)
        )
        existing = existing_result.scalar_one_or_none()
        if existing and existing.ingestion_status == "COMPLETED":
            logger.info("Document already ingested | document_id=%s", existing.document_id)
            return IngestResponse(
                document_id=existing.document_id,
                file_name=existing.file_name,
                ingestion_status=existing.ingestion_status,
                page_count=existing.page_count,
                is_scanned=existing.is_scanned or False,
                message="Document already ingested — skipping",
                success=True,
            )

        document_id = uuid.uuid4()
        document = Document(
            document_id=document_id,
            file_name=request.file_name,
            original_file_name=request.file_name,
            document_type=request.document_type or "PDF",
            mime_type="application/pdf",
            source_system=request.source_system or "local",
            storage_uri=str(file_path),
            document_hash=doc_hash,
            ingestion_status="PROCESSING",
            metadata_json=request.metadata or {},
        )
        session.add(document)
        await session.flush()

        run = ProcessingRun(
            run_id=uuid.uuid4(),
            document_id=document_id,
            run_type="INGESTION",
            status="STARTED",
            start_timestamp=_utcnow(),
        )
        session.add(run)
        await session.flush()

        try:
            logger.info("Extracting text | file=%s", request.file_name)
            pages, is_scanned = extract_pdf_text(file_path)
            page_count = len(pages)

            document.page_count = page_count
            document.is_scanned = is_scanned
            await session.flush()

            # Build chunks across all pages
            all_chunk_texts: list[str] = []
            chunk_page_map: list[int] = []
            for page_num, page_text in pages:
                if not page_text.strip():
                    continue
                for chunk in _chunk_text(page_text, settings.chunk_size, settings.chunk_overlap):
                    all_chunk_texts.append(chunk)
                    chunk_page_map.append(page_num)

            logger.info("Chunking complete | chunks=%d file=%s", len(all_chunk_texts), request.file_name)

            # Batch embed all chunks
            embeddings = await get_embeddings_batch(all_chunk_texts)

            # Persist chunks and embeddings
            for seq, (chunk_text, page_num, embedding) in enumerate(
                zip(all_chunk_texts, chunk_page_map, embeddings)
            ):
                chunk_id = uuid.uuid4()
                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    chunk_sequence=seq,
                    page_start=page_num,
                    page_end=page_num,
                    chunk_text=chunk_text,
                    token_count=len(chunk_text.split()),
                )
                session.add(chunk)
                await session.flush()

                session.add(ChunkEmbedding(
                    embedding_id=uuid.uuid4(),
                    chunk_id=chunk_id,
                    embedding_type="dense",
                    embedding_model=settings.embedding_model,
                    embedding=embedding,
                ))

            document.ingestion_status = "COMPLETED"
            document.updated_timestamp = _utcnow()
            run.status = "COMPLETED"
            run.end_timestamp = _utcnow()
            await session.commit()

            logger.info(
                "IngestionService.ingest_document EXIT | document_id=%s chunks=%d pages=%d scanned=%s",
                document_id, len(all_chunk_texts), page_count, is_scanned,
            )

            return IngestResponse(
                document_id=document_id,
                file_name=request.file_name,
                ingestion_status="COMPLETED",
                page_count=page_count,
                chunk_count=len(all_chunk_texts),
                is_scanned=is_scanned,
                message="Document ingested successfully",
                success=True,
            )

        except Exception as exc:
            logger.error("Ingestion failed | file=%s error=%s", request.file_name, exc, exc_info=True)
            document.ingestion_status = "FAILED"
            run.status = "FAILED"
            run.error_message = str(exc)
            run.end_timestamp = _utcnow()
            await session.commit()
            raise
