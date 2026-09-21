from opentelemetry import metrics

# Must be created after setup_telemetry() has called metrics.set_meter_provider(),
# so this module is only imported (directly or transitively) from code paths
# that run after app.py's setup_telemetry("ai-document-services") call.
_meter = metrics.get_meter("ai-document-services")

documents_ingested_total = _meter.create_counter(
    "documents_ingested_total",
    unit="1",
    description="Documents ingested, labeled by outcome (completed/failed/already_ingested)",
)

chunks_embedded_total = _meter.create_counter(
    "chunks_embedded_total",
    unit="1",
    description="Document chunks embedded and persisted during ingestion",
)

document_ingestion_duration_seconds = _meter.create_histogram(
    "document_ingestion_duration_seconds",
    unit="s",
    description="End-to-end duration of a single document ingestion run",
)
