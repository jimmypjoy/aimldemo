import logging

from llm.llm_client import LLMClient
from models.llm.llm_request import LLMRequest
from models.llm.llm_response import LLMResponse

logger = logging.getLogger(__name__)

_client = LLMClient()


class LLMService:

    def invoke_llm(self, request: LLMRequest) -> LLMResponse:
        logger.info("LLMService.invoke_llm ENTRY | model=%s user_role=%s query_preview=%.80s",
                    request.llm_model.model_name, request.user_role, request.query)

        response = _client.invoke_llm(request)

        logger.info("LLMService.invoke_llm EXIT | success=%s response_time=%.3fs",
                    response.success, response.response_time)
        return response
