import functools
import inspect
import time

from opentelemetry import metrics, trace
from opentelemetry.trace import Status, StatusCode

# Instrumentation-scope name: "which library produced this telemetry",
# distinct from the resource's service.name ("which deployed service
# instance"). Every project using track_tool_call shares this scope name;
# `setup()`'s resource.service.name is what actually distinguishes them in
# Grafana.
_meter = metrics.get_meter("ai_otel_observability.tool_tracking")

tool_calls_total = _meter.create_counter(
    "tool_calls_total",
    unit="1",
    description="Tool invocations, labeled by tool_name and success",
)

tool_call_duration_seconds = _meter.create_histogram(
    "tool_call_duration_seconds",
    unit="s",
    description="Duration of a single tool invocation, labeled by tool_name",
)


def track_tool_call(tool_name: str):
    """Wrap an MCP/RPC tool function (sync or async) with call-count/
    duration metrics, an identifying span attribute, and span error marking
    -- without touching the tool's own implementation.

    Apply at tool-registration time (e.g. `mcp.add_tool(track_tool_call(name)(func))`)
    so every tool in a project is covered uniformly. This can't be fully
    automatic: a generic instrumentor sees "a request arrived at the one
    /mcp endpoint," not "which of my tools this particular call dispatches
    to" -- that mapping only exists at the point a project registers its
    own tools, which is exactly where this decorator is meant to be used.
    """
    def decorator(func):
        # FastMCP (and similar RPC frameworks) build each tool's caller-facing
        # schema from the wrapped function's signature and docstring, so the
        # wrapper must expose the original ones exactly. functools.wraps
        # copies __doc__/__name__ and sets __wrapped__, but inspect.signature()
        # checks __signature__ first specifically for cases like this, so it's
        # set explicitly here rather than relying on every caller following
        # __wrapped__.
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    _record(tool_name, start, success=True)
                    return result
                except Exception as exc:
                    _record(tool_name, start, success=False, exc=exc)
                    raise
            async_wrapper.__signature__ = inspect.signature(func)
            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                _record(tool_name, start, success=True)
                return result
            except Exception as exc:
                _record(tool_name, start, success=False, exc=exc)
                raise
        sync_wrapper.__signature__ = inspect.signature(func)
        return sync_wrapper

    return decorator


def _record(tool_name: str, start: float, success: bool, exc: Exception | None = None) -> None:
    elapsed = time.perf_counter() - start
    tool_calls_total.add(1, {"tool_name": tool_name, "success": success})
    tool_call_duration_seconds.record(elapsed, {"tool_name": tool_name})

    # Identifies which tool this span belongs to, on the current span itself
    # (normally the incoming request span) -- without this, every tool call
    # through a single-endpoint RPC protocol like MCP looks identical in
    # Tempo (e.g. a generic "POST /mcp"), since the tool name only exists
    # inside the request body, invisible to generic HTTP auto-instrumentation.
    span = trace.get_current_span()
    span.set_attribute("gen_ai.tool.name", tool_name)
    if exc is not None:
        span.record_exception(exc)
        span.set_status(Status(StatusCode.ERROR, str(exc)))
