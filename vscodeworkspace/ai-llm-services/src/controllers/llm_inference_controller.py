import logging

from fastapi import APIRouter, HTTPException

from models.llm.llm_request import LLMRequest
from models.llm.llm_response import LLMResponse
from services.llm_service import LLMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/llm", tags=["LLM Inference"])

_service = LLMService()


@router.post("/invoke", response_model=LLMResponse)
def invoke_llm(request: LLMRequest) -> LLMResponse:
    logger.info("POST /api/v1/llm/invoke ENTRY | model=%s user_role=%s",
                request.llm_model.model_name, request.user_role)
    try:
        response = _service.invoke_llm(request)
        logger.info("POST /api/v1/llm/invoke EXIT | success=%s response_time=%.3fs",
                    response.success, response.response_time)
        return response
    except Exception as exc:
        logger.error("POST /api/v1/llm/invoke UNHANDLED ERROR | %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
