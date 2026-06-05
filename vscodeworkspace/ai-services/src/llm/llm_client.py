import logging
import time

from openai import OpenAI

from models.llm.llm_request import LLMRequest
from models.llm.llm_response import LLMResponse

logger = logging.getLogger(__name__)

_openai_client = OpenAI()


class LLMClient:

    def invoke_llm(self, request: LLMRequest) -> LLMResponse:
        logger.info("LLMClient.invoke_llm ENTRY | model_family=%s model=%s user_role=%s",
                    request.llm_model.family, request.llm_model.model_name, request.user_role)

        if request.llm_model.family == "GEMINI":
            response = self._invoke_gemini(request)
        else:
            response = self._invoke_gpt(request)

        logger.info("LLMClient.invoke_llm EXIT | success=%s response_time=%.3fs",
                    response.success, response.response_time)
        return response

    def _invoke_gpt(self, request: LLMRequest) -> LLMResponse:
        logger.info("_invoke_gpt ENTRY | model=%s", request.llm_model.model_name)
        start = time.perf_counter()
        try:
            messages = [
                {"role": "system", "content": request.prompt},
                {"role": request.user_role, "content": request.query},
            ]
            logger.info("Sending request to OpenAI | model=%s messages=%s",
                        request.llm_model.model_name, messages)

            completion = _openai_client.chat.completions.create(
                model=request.llm_model.model_name,
                messages=messages,
            )
            response_text = completion.choices[0].message.content
            elapsed = time.perf_counter() - start

            logger.info("Received response from OpenAI | model=%s response_time=%.3fs response_preview=%.100s",
                        request.llm_model.model_name, elapsed, response_text)

            return LLMResponse(
                llm_response=response_text,
                llm_model=request.llm_model,
                response_time=elapsed,
                success=True,
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("_invoke_gpt FAILED | model=%s response_time=%.3fs error=%s",
                         request.llm_model.model_name, elapsed, exc, exc_info=True)
            return LLMResponse(
                llm_response="",
                llm_model=request.llm_model,
                response_time=elapsed,
                success=False,
                exception_message=str(exc),
            )

    def _invoke_gemini(self, request: LLMRequest) -> LLMResponse:
        msg = "GEMINI invocation not yet supported by this service"
        logger.warning("_invoke_gemini | model=%s | %s", request.llm_model.model_name, msg)
        return LLMResponse(
            llm_response=msg,
            llm_model=request.llm_model,
            response_time=0.0,
            success=False,
            exception_message=msg,
        )
