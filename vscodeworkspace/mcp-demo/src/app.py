import logging

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Deferred imports: must run after load_dotenv() so settings and the module-level
# httpx client initialise with environment variables already in place.
from config.settings import get_settings  # noqa: E402
from tools.company_details_tool import get_company_details  # noqa: E402
from tools.document_query_tool import query_document  # noqa: E402
from tools.market_capitalization_tool import market_capitalization_web_search  # noqa: E402

settings = get_settings()

mcp = FastMCP(
    name="document-query-mcp",
    host=settings.mcp_host,
    port=settings.mcp_port,
)

mcp.add_tool(query_document)
mcp.add_tool(market_capitalization_web_search)
mcp.add_tool(get_company_details)

logger.info(
    "document-query-mcp initialised | document_service_url=%s",
    settings.document_service_url,
)
