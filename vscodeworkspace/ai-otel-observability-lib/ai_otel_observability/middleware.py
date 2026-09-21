import logging

from opentelemetry import baggage, trace

logger = logging.getLogger("ai_otel_observability.request")


def _log_request(path: str | None) -> None:
    # Logs whatever business-context baggage is present (adk.session_id,
    # review.key, case.id, ...) generically -- this library doesn't know any
    # one team's business key, so it logs the whole baggage set rather than
    # a hardcoded field name. Always logs trace_id too, since that's present
    # on every request regardless of whether set_business_context() was
    # ever called.
    trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
    logger.info(
        "request received | trace_id=%s context=%s path=%s",
        trace_id,
        dict(baggage.get_all()),
        path,
    )


class RequestTraceLoggingMiddleware:
    """ASGI middleware that logs the trace_id and business-context baggage
    once per request, at the entry point, for troubleshooting/traceability
    when correlating a service's logs to Grafana.

    Use this directly for a raw ASGI app that has no FastAPI `app` to hang a
    decorator off of (e.g. `mcp.streamable_http_app()`). Must sit *inside*
    OpenTelemetryMiddleware (or equivalent) so trace/baggage context has
    already been extracted from the incoming request by the time this runs:

        asgi_app = OpenTelemetryMiddleware(RequestTraceLoggingMiddleware(raw_app))
    """

    def __init__(self, app) -> None:
        self._app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            _log_request(scope.get("path"))
        await self._app(scope, receive, send)


def instrument_fastapi_app(app) -> None:
    """Instruments a FastAPI app: standard FastAPIInstrumentor, plus the
    same entry-point trace/baggage logging as RequestTraceLoggingMiddleware.

    Lazily imports opentelemetry-instrumentation-fastapi, so a project that
    doesn't install the `fastapi` extra never pays for it unless this is
    actually called.
    """
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    FastAPIInstrumentor.instrument_app(app)

    @app.middleware("http")
    async def _log_request_trace_context(request, call_next):
        _log_request(request.url.path)
        return await call_next(request)
