import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from telemetry import setup_telemetry  # noqa: E402

setup_telemetry("ai-llm-services")

from fastapi import FastAPI  # noqa: E402
from opentelemetry import baggage, trace  # noqa: E402
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # noqa: E402
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor  # noqa: E402

logger = logging.getLogger(__name__)

HTTPXClientInstrumentor().instrument()

# Deferred imports: must run after load_dotenv() and setup_telemetry() so that
# module-level singletons (OpenAI client, Langfuse client, loggers) initialise with
# env vars and logging/tracing already configured.
from controllers.llm_inference_controller import router as llm_router  # noqa: E402
from llm.llm_client import _langfuse  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("AI Services shutting down | flushing Langfuse traces")
    _langfuse.shutdown()


app = FastAPI(title="AI Services", version="1.0.0", lifespan=lifespan)
app.include_router(llm_router)
FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def log_request_trace_context(request, call_next):
    # Entry-point log: one line per request carrying the trace_id (always
    # present) alongside the adk.session_id baggage propagated from
    # adk-agent-demo, so this service's logs can be grepped/searched in
    # Grafana the same way as the other 3 services.
    trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
    logger.info(
        "request received | trace_id=%s adk_session_id=%s path=%s",
        trace_id,
        baggage.get_baggage("adk.session_id"),
        request.url.path,
    )
    return await call_next(request)


logger.info(
    "FastAPI app initialised | OPENAI_API_KEY configured=%s | GEMINI_API_KEY configured=%s | "
    "LANGFUSE_PUBLIC_KEY configured=%s",
    bool(os.getenv("OPENAI_API_KEY")), bool(os.getenv("GEMINI_API_KEY")),
    bool(os.getenv("LANGFUSE_PUBLIC_KEY")),
)


@app.get("/health")
def health():
    logger.info("/health endpoint called")
    return {"status": "ok"}
