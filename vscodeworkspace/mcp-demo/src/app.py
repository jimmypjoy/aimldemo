import logging

from dotenv import load_dotenv

load_dotenv()

from telemetry import setup_telemetry  

setup_telemetry("mcp-demo")

from mcp.server.fastmcp import FastMCP  
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor 

logger = logging.getLogger(__name__)

HTTPXClientInstrumentor().instrument()

# Deferred imports: must run after load_dotenv() and setup_telemetry() so settings
# and the module-level httpx client initialise with env vars and tracing already
# configured.
from config.settings import get_settings  
from metrics import track_tool_call  
from tools.company_details_tool import get_company_details  
from tools.document_query_tool import query_document  
from tools.market_capitalization_tool import market_capitalization_web_search  

settings = get_settings()

mcp = FastMCP(
    name="document-query-mcp",
    host=settings.mcp_host,
    port=settings.mcp_port,
)

# Wrapped with tool_calls_total / tool_call_duration_seconds metrics at
# registration time, so every tool is covered uniformly without touching each
# tool's own implementation.
mcp.add_tool(track_tool_call("query_document")(query_document))
mcp.add_tool(track_tool_call("market_capitalization_web_search")(market_capitalization_web_search))
mcp.add_tool(track_tool_call("get_company_details")(get_company_details))

logger.info(
    "document-query-mcp initialised | document_service_url=%s",
    settings.document_service_url,
)
