import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Deferred imports: must run after load_dotenv() and logging.basicConfig() so that
# module-level singletons (OpenAI client, Langfuse client, loggers) initialise with
# env vars and logging already configured.
from controllers.llm_inference_controller import router as llm_router  # noqa: E402
from llm.llm_client import _langfuse  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("AI Services shutting down | flushing Langfuse traces")
    _langfuse.shutdown()


app = FastAPI(title="AI Services", version="1.0.0", lifespan=lifespan)
app.include_router(llm_router)

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
