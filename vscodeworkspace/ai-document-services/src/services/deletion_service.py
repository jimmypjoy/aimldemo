import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.entities.chunk_embedding_entity import ChunkEmbedding
from db.entities.document_chunk_entity import DocumentChunk
from db.entities.document_entity import Document
from db.entities.processing_run_entity import ProcessingRun
from models.document.ingest_response import DeleteResponse

logger = logging.getLogger(__name__)


class DeletionService:

    async def delete_document(self, file_name: str, session: AsyncSession) -> DeleteResponse:
        logger.info("DeletionService.delete_document ENTRY | file_name=%s", file_name)

        result = await session.execute(
            select(Document).where(Document.file_name == file_name)
        )
        document = result.scalar_one_or_none()

        if document is None:
            raise FileNotFoundError(f"No document found with file_name: {file_name}")

        document_id = document.document_id

        # 1 — delete chunk_embeddings (FK → document_chunks)
        chunk_id_rows = await session.execute(
            select(DocumentChunk.chunk_id).where(DocumentChunk.document_id == document_id)
        )
        chunk_ids = [row[0] for row in chunk_id_rows.all()]

        embeddings_deleted = 0
        if chunk_ids:
            emb_result = await session.execute(
                delete(ChunkEmbedding).where(ChunkEmbedding.chunk_id.in_(chunk_ids))
            )
            embeddings_deleted = emb_result.rowcount
            logger.info("Deleted chunk_embeddings | count=%d document_id=%s", embeddings_deleted, document_id)

        # 2 — delete document_chunks (FK → documents)
        chunk_result = await session.execute(
            delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )
        chunks_deleted = chunk_result.rowcount
        logger.info("Deleted document_chunks | count=%d document_id=%s", chunks_deleted, document_id)

        # 3 — delete processing_runs (FK → documents)
        run_result = await session.execute(
            delete(ProcessingRun).where(ProcessingRun.document_id == document_id)
        )
        runs_deleted = run_result.rowcount
        logger.info("Deleted processing_runs | count=%d document_id=%s", runs_deleted, document_id)

        # 4 — delete the document itself
        await session.delete(document)
        await session.commit()

        logger.info(
            "DeletionService.delete_document EXIT | file_name=%s embeddings=%d chunks=%d runs=%d",
            file_name, embeddings_deleted, chunks_deleted, runs_deleted,
        )

        return DeleteResponse(
            file_name=file_name,
            chunks_deleted=chunks_deleted,
            embeddings_deleted=embeddings_deleted,
            processing_runs_deleted=runs_deleted,
            message=f"Document '{file_name}' and all related data deleted successfully",
            success=True,
        )
