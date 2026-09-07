import logging

from config.settings import get_settings
from llm.llm_client import LLMClient

logger = logging.getLogger(__name__)
settings = get_settings()

_client = LLMClient()

_SYSTEM_PROMPT = """You are a financial research assistant with access to a live web search tool.

You MUST use web search to find the company's CURRENT market capitalization. \
Do NOT answer from your own pretrained knowledge — it may be outdated or wrong, \
and market capitalization changes daily with the stock price.

Steps:
1. Search the web for the company's current, up-to-date market capitalization (in USD).
2. Convert the figure to billions of US dollars, rounded to 2 decimal places.
3. Respond in EXACTLY this format, with no extra commentary:
   Company: <company name>
   Market Capitalization: $<value> billion USD
   As Of: <date of the figure you found, or "unknown" if not stated>
   Source: <name of the site/source the figure came from>

If web search does not return a reliable figure, respond with exactly:
   Company: <company name>
   Market Capitalization: Not found
"""


async def market_capitalization_web_search(company_name: str) -> str:
    """
    Look up a company's current market capitalization via a live web search
    and return it in billions of USD.

    Uses web search grounding rather than the LLM's pretrained knowledge, since
    market capitalization changes daily and a static model would otherwise
    return stale or fabricated figures.

    Args:
        company_name: The name of the company to look up
                      (e.g. "Apple", "Microsoft", "Tesla").

    Returns:
        A short plain-text report with the company's market capitalization in
        billions of USD, the as-of date, and the web source it was found from.
    """
    logger.info("market_capitalization_web_search ENTRY | company_name=%s", company_name)

    result = await _client.invoke(
        prompt=_SYSTEM_PROMPT,
        query=f"What is the current market capitalization of {company_name}?",
        model=settings.web_search_model,
        use_web_search=True,
    )

    logger.info("market_capitalization_web_search EXIT | company_name=%s", company_name)
    return result
