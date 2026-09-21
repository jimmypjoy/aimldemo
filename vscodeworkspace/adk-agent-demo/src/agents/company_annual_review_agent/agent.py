import logging
import sys
from datetime import date
from pathlib import Path

_src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_src_dir))

from dotenv import load_dotenv

load_dotenv(_src_dir.parent / ".env")

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from opentelemetry import baggage, trace
from opentelemetry.context import attach
from opentelemetry.sdk.trace import SpanProcessor

from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class BaggageSpanProcessor(SpanProcessor):
    """Promotes every OTel Baggage entry onto each span as it starts, so
    adk.session_id becomes a searchable Tempo span attribute instead of just
    in-flight context. Same processor as the other 3 services (see
    mcp-demo/src/telemetry.py); registered here instead of a telemetry.py
    since this project has none -- its TracerProvider is set up by the
    `opentelemetry-instrument` wrapper (or ADK's own fallback) before this
    module is imported, so it's already available to attach to by the time
    this file loads.
    """

    def on_start(self, span, parent_context=None) -> None:
        for key, value in baggage.get_all(parent_context).items():
            span.set_attribute(key, value)


_tracer_provider = trace.get_tracer_provider()
if hasattr(_tracer_provider, "add_span_processor"):
    _tracer_provider.add_span_processor(BaggageSpanProcessor())

_SKILL_PATH = _src_dir / "skills" / "company_annual_review" / "SKILL.md"
_SKILL_CONTENT = _SKILL_PATH.read_text(encoding="utf-8")


def build_instruction(context: ReadonlyContext) -> str:
    today = date.today().isoformat()
    return f"Today's date is {today}.\n\n{_SKILL_CONTENT}"


def mcp_session_headers(readonly_context: ReadonlyContext) -> dict[str, str]:
    """Keys the pooled MCP connection to this ADK session.

    MCPSessionManager pools/reuses one persistent connection per distinct
    header set (it hashes the headers to a cache key), and that connection's
    background writer task freezes whatever OTel context (trace + baggage)
    was active the moment the connection was first opened -- forever, for
    every later tool call through it, regardless of which session queued the
    call. Without this, one connection gets opened on the very first tool
    call the process ever makes and is then reused across every subsequent
    ADK session, so trace_id/baggage set here never reach mcp-demo past that
    first call.

    Returning a header that varies by ADK session forces a fresh connection
    (and a freshly-frozen background task) per session, so the freeze point
    lines up with "start of this session" instead of "start of this process".
    """
    return {"X-ADK-Session-Id": readonly_context.session.id}


def log_session_trace(callback_context: CallbackContext):
    """Attaches the ADK session id to OTel Baggage once per session and logs
    it alongside the trace_id, so both ids propagate end-to-end and are
    searchable as span attributes / log fields in every service.

    Registered as before_agent_callback, not before_model_callback: ADK calls
    get_tools() on the MCPToolset (opening the MCP connection) while building
    the LLM request, which happens *before* before_model_callback fires. That
    connection's background writer task freezes whatever OTel context existed
    at that moment -- so if baggage were attached in before_model_callback, it
    would already be too late, and the connection (fresh per session thanks to
    mcp_session_headers) would freeze with no baggage on it. before_agent_callback
    runs earlier, ahead of tool discovery, so the baggage is in place in time.
    """
    if callback_context.state.get("adk_session_id_logged"):
        return None

    session_id = callback_context.session.id
    attach(baggage.set_baggage("adk.session_id", session_id))
    callback_context.state["adk_session_id_logged"] = True

    trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
    logger.info("#"*100)
    logger.info(
        "session started | trace_id=%s adk_session_id=%s",
        trace_id,
        session_id,
    )
    logger.info("#"*100)
    return None


root_agent = Agent(
    name="company_annual_review_agent",
    model=settings.agent_model,
    description=(
        "Specialized agent that produces a Company Annual Review summary "
        "(revenue, market capitalization, internal rating, analyst name) "
        "using only the tools exposed by the mcp-demo MCP server."
    ),
    instruction=build_instruction,
    before_agent_callback=log_session_trace,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=f"{settings.mcp_server_url}/mcp"
            ),
            header_provider=mcp_session_headers,
        ),
    ],
)
