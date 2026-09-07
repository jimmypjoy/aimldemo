import logging

import httpx

from config.settings import get_settings
from models.document_query_model import DocumentQueryRequest, DocumentQueryResponse

logger = logging.getLogger(__name__)
settings = get_settings()

_client = httpx.AsyncClient(base_url=settings.document_service_url, timeout=60.0)


class DocumentQueryService:

    async def query(self, request: DocumentQueryRequest) -> DocumentQueryResponse:
        logger.info(
            "DocumentQueryService.query ENTRY | query=%.60s file_name=%s top_k=%d",
            request.query, request.file_name, request.top_k,
        )
        resp = await _client.post(
            "/api/v1/documents/query",
            json=request.model_dump(exclude_none=True),
        )
        resp.raise_for_status()
        response = DocumentQueryResponse.model_validate(resp.json())

        logger.info(
            "DocumentQueryService.query EXIT | total_results=%d llm_answered=%s",
            response.total_results, response.llm_answer is not None,
        )
        return response
