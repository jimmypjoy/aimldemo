import logging
import os
import time

from google import genai
from google.genai import types
from langfuse import Langfuse, observe
from openai import OpenAI

from models.llm.llm_request import LLMRequest
from models.llm.llm_response import LLMResponse

logger = logging.getLogger(__name__)

_openai_client = OpenAI()
_genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_langfuse = Langfuse()


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

    @observe(name="invoke-gpt", as_type="generation", capture_input=False, capture_output=False)
    def _invoke_gpt(self, request: LLMRequest) -> LLMResponse:
        logger.info("_invoke_gpt ENTRY | model=%s", request.llm_model.model_name)
        start = time.perf_counter()
        messages = [
            {"role": "system", "content": request.prompt},
            {"role": request.user_role, "content": request.query},
        ]
        _langfuse.update_current_generation(
            model=request.llm_model.model_name,
            input=messages,
            model_parameters={"use_web_search": request.use_web_search},
        )

        try:
            logger.info("Sending request to OpenAI | model=%s messages=%s",
                        request.llm_model.model_name, messages)

            kwargs = {"web_search_options": {}} if request.use_web_search else {}
            completion = _openai_client.chat.completions.create(
                model=request.llm_model.model_name,
                messages=messages,
                **kwargs,
            )
            response_text = completion.choices[0].message.content
            elapsed = time.perf_counter() - start

            logger.info("Received response from OpenAI | model=%s response_time=%.3fs response_preview=%.100s",
                        request.llm_model.model_name, elapsed, response_text)

            usage = completion.usage
            _langfuse.update_current_generation(
                output=response_text,
                usage_details={
                    "input": usage.prompt_tokens,
                    "output": usage.completion_tokens,
                    "total": usage.total_tokens,
                } if usage else None,
            )

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
            _langfuse.update_current_generation(level="ERROR", status_message=str(exc))
            return LLMResponse(
                llm_response="",
                llm_model=request.llm_model,
                response_time=elapsed,
                success=False,
                exception_message=str(exc),
            )

    @observe(name="invoke-gemini", as_type="generation", capture_input=False, capture_output=False)
    def _invoke_gemini(self, request: LLMRequest) -> LLMResponse:
        logger.info("_invoke_gemini ENTRY | model=%s", request.llm_model.model_name)
        start = time.perf_counter()
        _langfuse.update_current_generation(
            model=request.llm_model.model_name,
            input=request.query,
            metadata={"system_instruction": request.prompt},
        )

        try:
            response = _genai_client.models.generate_content(
                model=request.llm_model.model_name,
                contents=request.query,
                config=types.GenerateContentConfig(system_instruction=request.prompt),
            )
            response_text = response.text
            elapsed = time.perf_counter() - start

            logger.info("Received response from Gemini | model=%s response_time=%.3fs response_preview=%.100s",
                        request.llm_model.model_name, elapsed, response_text)

            usage = response.usage_metadata
            _langfuse.update_current_generation(
                output=response_text,
                usage_details={
                    "input": usage.prompt_token_count,
                    "output": usage.candidates_token_count,
                    "total": usage.total_token_count,
                } if usage else None,
            )

            return LLMResponse(
                llm_response=response_text,
                llm_model=request.llm_model,
                response_time=elapsed,
                success=True,
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("_invoke_gemini FAILED | model=%s response_time=%.3fs error=%s",
                         request.llm_model.model_name, elapsed, exc, exc_info=True)
            _langfuse.update_current_generation(level="ERROR", status_message=str(exc))
            return LLMResponse(
                llm_response="",
                llm_model=request.llm_model,
                response_time=elapsed,
                success=False,
                exception_message=str(exc),
            )
