import logging
import time

import httpx

from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_client = httpx.AsyncClient(base_url=settings.llm_service_url, timeout=60.0)


class LLMClient:

    async def invoke(self, prompt: str, query: str, model: str, use_web_search: bool = False) -> str:
        logger.info("LLMClient.invoke ENTRY | model=%s use_web_search=%s", model, use_web_search)
        start = time.perf_counter()
        try:
            resp = await _client.post(
                "/api/v1/llm/invoke",
                json={
                    "query": query,
                    "prompt": prompt,
                    "llm_model": model,
                    "use_web_search": use_web_search,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            elapsed = time.perf_counter() - start

            if not data.get("success"):
                raise RuntimeError(data.get("exception_message") or "LLM invocation failed")

            logger.info("LLMClient.invoke EXIT | model=%s time=%.3fs", model, elapsed)
            return data["llm_response"]
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("LLMClient.invoke FAILED | model=%s time=%.3fs error=%s",
                         model, elapsed, exc, exc_info=True)
            raise
