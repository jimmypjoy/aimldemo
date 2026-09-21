from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

from opentelemetry import baggage, trace
from opentelemetry.context import attach

if TYPE_CHECKING:
    # Only needed for type hints -- keeps google-adk an optional dependency
    # for any project that imports this module (every ADK agent project
    # will have it installed anyway, but the import shouldn't be required
    # just to read this module's type annotations).
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.agents.readonly_context import ReadonlyContext

logger = logging.getLogger(__name__)


def make_mcp_session_headers(header_name: str = "X-ADK-Session-Id"):
    """Returns an MCPToolset `header_provider` that keys the pooled MCP
    connection to the current ADK session.

    MCPSessionManager pools/reuses one persistent connection per distinct
    header set (it hashes the headers to a cache key), and that connection's
    background writer task freezes whatever OTel context (trace + baggage)
    was active the moment the connection was first opened -- forever, for
    every later tool call through it, regardless of which session queued the
    call. Without this, one connection opens on the process's very first
    tool call and is reused across every subsequent ADK session, so
    trace_id/baggage set later never reach the MCP server past that first
    call.

    Returning a header that varies by ADK session forces a fresh connection
    (and a freshly-frozen background task) per session, so the freeze point
    lines up with "start of this session" instead of "start of this
    process." Pair with `make_session_baggage_callback()` as
    `before_agent_callback` -- baggage has to be attached *before* this
    fires (ADK opens the MCP connection while discovering tool schemas,
    which happens before `before_model_callback` but after
    `before_agent_callback`).
    """
    def _provider(readonly_context: "ReadonlyContext") -> dict[str, str]:
        return {header_name: readonly_context.session.id}

    return _provider


# Ready-to-use default: `MCPToolset(..., header_provider=mcp_session_headers)`.
mcp_session_headers = make_mcp_session_headers()


def make_session_baggage_callback(
    baggage_key: str = "adk.session_id",
    value_fn: "Callable[[CallbackContext], str | None] | None" = None,
):
    """Returns a `before_agent_callback` that attaches a business-context
    value to OTel Baggage once per session and logs it alongside the
    trace_id.

    Registered as `before_agent_callback`, not `before_model_callback`: ADK
    calls get_tools() on the MCPToolset (opening the MCP connection) while
    building the LLM request, which happens *before* before_model_callback
    fires. That connection's background writer task freezes whatever OTel
    context existed at that moment -- so if baggage were attached in
    before_model_callback, it would already be too late. before_agent_callback
    runs earlier, ahead of tool discovery, so the baggage is in place in time.

    Args:
        baggage_key: The namespaced OTel Baggage key to attach the value
            under (and the field name it's logged/searchable as downstream).
            Defaults to the ADK session id; pass a different key (and
            value_fn) for a team whose natural business key is something
            else, e.g. a case id pulled from session state.
        value_fn: How to derive the value from the CallbackContext. Defaults
            to the ADK session id. Return None/empty to skip attaching for
            this invocation (e.g. the value isn't known yet).
    """
    state_flag = f"_ai_otel_{baggage_key}_attached"

    def _default_value_fn(callback_context: "CallbackContext") -> str:
        return callback_context.session.id

    resolve_value = value_fn or _default_value_fn

    def _callback(callback_context: "CallbackContext") -> None:
        if callback_context.state.get(state_flag):
            return None

        value = resolve_value(callback_context)
        if not value:
            return None

        attach(baggage.set_baggage(baggage_key, value))
        callback_context.state[state_flag] = True

        trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
        logger.info(
            "session started | trace_id=%s %s=%s",
            trace_id,
            baggage_key,
            value,
        )
        return None

    return _callback


# Ready-to-use default: `Agent(..., before_agent_callback=attach_session_baggage)`.
attach_session_baggage = make_session_baggage_callback()
