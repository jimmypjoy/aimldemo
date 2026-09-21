import logging

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from ai_otel_observability.baggage import BaggageSpanProcessor, set_business_context
from ai_otel_observability.middleware import RequestTraceLoggingMiddleware, instrument_fastapi_app
from ai_otel_observability.tool_tracking import track_tool_call

__version__ = "0.1.0"

__all__ = [
    "setup",
    "BaggageSpanProcessor",
    "set_business_context",
    "RequestTraceLoggingMiddleware",
    "instrument_fastapi_app",
    "track_tool_call",
]

_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "trace_id=%(otelTraceID)s span_id=%(otelSpanID)s | %(message)s"
)

# Shortened from the SDK default of 60s so metrics show up in Grafana quickly.
_METRIC_EXPORT_INTERVAL_MILLIS = 5000


def setup(
    service_name: str,
    *,
    export_logs: bool = True,
    log_format: str = _LOG_FORMAT,
    sqlalchemy_engine=None,
) -> None:
    """Configures OTel traces, metrics, and (by default) logs for this
    process, and exports all of them via OTLP/gRPC to whatever
    OTEL_EXPORTER_OTLP_ENDPOINT points at.

    This is the one call every non-agent service makes, as early as
    possible -- before importing any modules that create their own spans,
    metrics, or that need instrumentation (httpx, a DB engine, etc), since
    those need the real providers already in place rather than falling back
    to no-op defaults. ADK agent processes use
    `ai_otel_observability.adk.setup_agent_telemetry()` instead, not this
    function directly -- see that module for why.

    Resource attributes (service.namespace, deployment.environment, ...)
    and the OTLP endpoint are read from the standard OTEL_RESOURCE_ATTRIBUTES
    / OTEL_EXPORTER_OTLP_ENDPOINT env vars -- deliberately not a library
    parameter, so this stays portable and consistent with any other OTel
    tooling/documentation a team already knows.

    Args:
        service_name: This process's service.name resource attribute. The
            one thing every project is required to pass explicitly.
        export_logs: Whether to also ship log records via OTLP (to Loki, in
            the default Grafana stack). Set False for a team that already
            has its own mature logging system and only wants OTel for
            traces/metrics -- console logging (with trace_id/span_id
            correlation) still happens either way.
        log_format: Console/OTLP log line format. Override only if a team
            wants a different layout than the trace/span-correlated default.
        sqlalchemy_engine: Pass a SQLAlchemy engine to also instrument it.
            Left out of the default instrumentor set (unlike httpx) because
            not every project uses a database, and auto-detecting engines
            reliably isn't possible without being handed one explicitly.
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
    # backwards (as the individual aimldemo services originally did) and every
    # logger.info() call in the app is silently dropped before it reaches any
    # handler, console or OTLP -- the one bug in this whole codebase that cost the
    # most time to track down, which is exactly why it's centralized here now.
    LoggingInstrumentor().instrument(set_logging_format=True, logging_format=log_format)

    if export_logs:
        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
        logging.getLogger().addHandler(
            LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
        )

    HTTPXClientInstrumentor().instrument()

    if sqlalchemy_engine is not None:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

        SQLAlchemyInstrumentor().instrument(engine=sqlalchemy_engine)
