from opentelemetry import metrics

# Must be created after setup_telemetry() has called metrics.set_meter_provider(),
# so this module is only imported (directly or transitively) from code paths
# that run after app.py's setup_telemetry("ai-llm-services") call.
_meter = metrics.get_meter("ai-llm-services")

llm_invocations_total = _meter.create_counter(
    "llm_invocations_total",
    unit="1",
    description="LLM invocations, labeled by model_family, model, and success",
)

llm_tokens_total = _meter.create_counter(
    "llm_tokens_total",
    unit="1",
    description="LLM tokens consumed, labeled by model and token_type (input/output)",
)

llm_call_duration_seconds = _meter.create_histogram(
    "llm_call_duration_seconds",
    unit="s",
    description="Duration of a single upstream LLM provider call",
)
