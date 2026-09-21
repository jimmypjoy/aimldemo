import functools
import inspect
import time

from opentelemetry import metrics, trace
from opentelemetry.trace import Status, StatusCode

# Must be created after setup_telemetry() has called metrics.set_meter_provider(),
# so this module is only imported (directly or transitively) from code paths
# that run after app.py's setup_telemetry("mcp-demo") call.
_meter = metrics.get_meter("mcp-demo")

tool_calls_total = _meter.create_counter(
    "tool_calls_total",
    unit="1",
    description="MCP tool invocations, labeled by tool_name and success",
)

tool_call_duration_seconds = _meter.create_histogram(
    "tool_call_duration_seconds",
    unit="s",
    description="Duration of a single MCP tool invocation, labeled by tool_name",
)


def track_tool_call(tool_name: str):
    """
    Wrap an MCP tool function (sync or async) with call-count/duration metrics
    and span error marking, without touching the tool's own implementation.
    Applied at registration time in app.py (mcp.add_tool(...)) so it covers
    every tool uniformly.
    """
    def decorator(func):
        # FastMCP builds each tool's LLM-facing schema from the wrapped
        # function's signature and docstring, so the wrapper must expose the
        # original ones exactly — functools.wraps copies __doc__/__name__ and
        # sets __wrapped__, but inspect.signature() is made to check
        # __signature__ first specifically for cases like this, so it's set
        # explicitly here rather than relying on every caller following
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
    if exc is not None:
        span = trace.get_current_span()
        span.record_exception(exc)
        span.set_status(Status(StatusCode.ERROR, str(exc)))
