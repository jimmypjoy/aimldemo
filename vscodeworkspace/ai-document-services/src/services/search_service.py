import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.entities.chunk_embedding_entity import ChunkEmbedding
from db.entities.document_chunk_entity import DocumentChunk
from db.entities.document_entity import Document
from llm.llm_client import LLMClient
from models.document.search_request import SearchRequest
from models.document.search_response import ChunkResult, SearchResponse
from util.embedding_util import get_embedding

logger = logging.getLogger(__name__)

_RAG_SYSTEM_PROMPT = """You are a helpful assistant. Answer the user's question using ONLY \
the document excerpts provided below as context. Respond in exactly the format the user \
requests (bullet points, a number, a single word, a paragraph, etc.). \
If the answer cannot be found in the provided excerpts, say: \
"I could not find that information in the provided document excerpts."

Context:
{context}"""

_llm_client = LLMClient()


class SearchService:

    async def search(self, request: SearchRequest, session: AsyncSession) -> SearchResponse:
        logger.info(
            "SearchService.search ENTRY | query_preview=%.60s file_name=%s top_k=%d llm_model=%s",
            request.query, request.file_name, request.top_k, request.llm_model,
        )

        query_embedding = await get_embedding(request.query)

        distance_col = ChunkEmbedding.embedding.cosine_distance(query_embedding).label("distance")

        stmt = (
            select(DocumentChunk, Document.file_name, distance_col)
            .join(ChunkEmbedding, DocumentChunk.chunk_id == ChunkEmbedding.chunk_id)
            .join(Document, DocumentChunk.document_id == Document.document_id)
            .where(Document.ingestion_status == "COMPLETED")
        )

        if request.file_name:
            stmt = stmt.where(Document.file_name == request.file_name)

        stmt = stmt.order_by("distance").limit(request.top_k)

        result = await session.execute(stmt)
        rows = result.all()

        chunk_results = [
            ChunkResult(
                chunk_id=row.DocumentChunk.chunk_id,
                document_id=row.DocumentChunk.document_id,
                file_name=row.file_name,
                chunk_sequence=row.DocumentChunk.chunk_sequence,
                page_start=row.DocumentChunk.page_start,
                page_end=row.DocumentChunk.page_end,
                chunk_text=row.DocumentChunk.chunk_text,
                similarity_score=round(1.0 - float(row.distance), 4),
            )
            for row in rows
        ]

        llm_answer: str | None = None
        llm_model_used: str | None = None

        if chunk_results:
            context_blocks = [
                f"[Source: {c.file_name} | Page {c.page_start} | Chunk {c.chunk_sequence}]\n{c.chunk_text}"
                for c in chunk_results
            ]
            context = "\n\n---\n\n".join(context_blocks)
            system_prompt = _RAG_SYSTEM_PROMPT.format(context=context)

            model = request.llm_model or "gemini-3.1-pro-preview"
            llm_model_used = model
            logger.info("Calling LLM for RAG answer | model=%s chunks=%d", model, len(chunk_results))
            llm_answer = await _llm_client.invoke(
                prompt=system_prompt,
                query=request.query,
                model=model,
            )

        logger.info("SearchService.search EXIT | results=%d llm_answered=%s", len(chunk_results), llm_answer is not None)

        return SearchResponse(
            query=request.query,
            file_name=request.file_name,
            results=chunk_results,
            total_results=len(chunk_results),
            llm_answer=llm_answer,
            llm_model=llm_model_used,
        )
