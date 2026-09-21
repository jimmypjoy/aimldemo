import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from telemetry import setup_telemetry  # noqa: E402

setup_telemetry("ai-document-services")

from fastapi import FastAPI  # noqa: E402
from opentelemetry import baggage, trace  # noqa: E402
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # noqa: E402
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor  # noqa: E402
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor  # noqa: E402

logger = logging.getLogger(__name__)

HTTPXClientInstrumentor().instrument()

# Deferred imports: must run after load_dotenv() and setup_telemetry() so that
# settings, the async DB engine, and logging/tracing all initialise with
# environment variables already in place.
from db.connection import engine  # noqa: E402
from controllers.document_controller import router as doc_router  # noqa: E402

SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "AI Document Services starting | DB configured=%s | OPENAI_API_KEY configured=%s",
        bool(os.getenv("DATABASE_URL")),
        bool(os.getenv("OPENAI_API_KEY")),
    )
    yield
    logger.info("AI Document Services shutting down")
    await engine.dispose()


app = FastAPI(
    title="AI Document Services",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(doc_router)
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


@app.get("/health")
def health():
    return {"status": "ok"}
