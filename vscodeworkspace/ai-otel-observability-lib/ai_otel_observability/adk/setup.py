from ai_otel_observability import setup as _setup


def setup_agent_telemetry(service_name: str, **kwargs) -> None:
    """Configures OTel for an ADK agent process -- same underlying setup as
    `ai_otel_observability.setup()`, but call this one from an ADK agent
    module (at import time, before `root_agent = Agent(...)` is
    constructed), not the CLI `opentelemetry-instrument` wrapper.

    Why not the CLI wrapper: ADK's own internal fallback
    (google.adk.telemetry.setup.maybe_set_otel_providers, invoked from
    google.adk.cli.api_server on every `adk web` startup) only activates
    providers that aren't already set -- it's a documented no-op if a
    TracerProvider/MeterProvider/LoggerProvider already exists. `opentelemetry-instrument`
    also tries to configure providers, from its own zero-code auto-instrumentation,
    and since it wraps the process before any of ADK's own code runs, it
    wins that race by default -- meaning ADK's internal setup silently never
    executes, and whether your own telemetry code (if any) wins instead
    depends on unrelated startup-order details neither side documents.

    Calling this function explicitly, early, removes the race entirely:
    this becomes the provider before either of the other two mechanisms
    gets a chance to run, so there's exactly one telemetry setup in effect,
    deliberately, not by accident of import order. Register `agent.py`'s
    entrypoint (agent_server.py or equivalent) to run `adk web` directly --
    no `opentelemetry-instrument` prefix needed.
    """
    _setup(service_name, **kwargs)
