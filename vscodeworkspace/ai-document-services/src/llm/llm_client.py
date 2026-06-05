import logging
import time

from openai import AsyncOpenAI

from llm.enums.llm_enum import LLMModel

logger = logging.getLogger(__name__)

_openai_client = AsyncOpenAI()


class LLMClient:

    async def invoke(self, prompt: str, query: str, model: LLMModel) -> str:
        logger.info("LLMClient.invoke ENTRY | model=%s", model.model_name)
        start = time.perf_counter()
        try:
            completion = await _openai_client.chat.completions.create(
                model=model.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                ],
                timeout=60,
            )
            response_text = completion.choices[0].message.content
            elapsed = time.perf_counter() - start
            logger.info("LLMClient.invoke EXIT | model=%s time=%.3fs", model.model_name, elapsed)
            return response_text
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("LLMClient.invoke FAILED | model=%s time=%.3fs error=%s",
                         model.model_name, elapsed, exc, exc_info=True)
            raise
