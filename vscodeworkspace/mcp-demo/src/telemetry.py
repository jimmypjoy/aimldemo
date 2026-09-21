import logging

from opentelemetry import baggage, metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "trace_id=%(otelTraceID)s span_id=%(otelSpanID)s | %(message)s"
)

# Shortened from the SDK default of 60s so metrics show up in Grafana quickly
# during local testing.
_METRIC_EXPORT_INTERVAL_MILLIS = 5000


class BaggageSpanProcessor(SpanProcessor):
    """Promotes every OTel Baggage entry onto each span as it starts.

    Baggage (adk.session_id, propagated from adk-agent-demo via the W3C
    baggage header) only travels in-context otherwise -- it never shows up as
    a Tempo-searchable span attribute unless something copies it on start,
    since by on_end the span is a read-only ReadableSpan.
    """

    def on_start(self, span, parent_context=None) -> None:
        for key, value in baggage.get_all(parent_context).items():
            span.set_attribute(key, value)


def setup_telemetry(service_name: str) -> None:
    """
    Configure global OTEL providers so this process exports traces, metrics,
    and logs via OTLP/gRPC to OTEL_EXPORTER_OTLP_ENDPOINT, and injects
    trace/span IDs into every log record for trace-log correlation in Grafana.

    Must be called before any other logging.basicConfig() call, since only
    the first call to basicConfig() in a process takes effect. Must also be
    called before instrumenting FastAPI/ASGI/httpx/etc., so those
    instrumentors pick up the tracer/meter providers configured here instead
    of falling back to no-op defaults.
    """
    resource = Resource.create({"service.name": service_name})

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BaggageSpanProcessor())
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(),
        export_interval_millis=_METRIC_EXPORT_INTERVAL_MILLIS,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Must run before the OTLP log handler is attached below: set_logging_format=True
    # calls logging.basicConfig(), which is a no-op once the root logger already has a
    # handler -- so this order is what actually gets a console StreamHandler attached
    # and raises the root logger's level from its WARNING default to INFO. Get this
    # backwards and every logger.info() call in the app is silently dropped before it
    # reaches any handler, console or OTLP.
    LoggingInstrumentor().instrument(set_logging_format=True, logging_format=_LOG_FORMAT)

    # Ship log records over OTLP as well, in addition to the console handler
    # basicConfig() just installed above.
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    logging.getLogger().addHandler(
        LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    )


class SessionTraceLoggingMiddleware:
    """ASGI middleware that logs the trace_id and adk.session_id baggage once
    per request, at the entry point, for troubleshooting/traceability when
    correlating this service's logs to Grafana.

    mcp.streamable_http_app() has no FastAPI `app` to hang an `@app.middleware`
    decorator off of (see server.py), so this wraps the ASGI app directly.
    Must sit *inside* OpenTelemetryMiddleware so the trace/baggage context is
    already extracted from the incoming request by the time this runs.
    """

    def __init__(self, app) -> None:
        self._app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
            logging.getLogger("mcp-demo.request").info(
                "request received | trace_id=%s adk_session_id=%s path=%s",
                trace_id,
                baggage.get_baggage("adk.session_id"),
                scope.get("path"),
            )
        await self._app(scope, receive, send)
