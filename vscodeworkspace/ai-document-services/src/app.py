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

# Deferred imports: must run after load_dotenv() so that settings and the
# async DB engine initialise with environment variables already in place.
from db.connection import engine  # noqa: E402
from controllers.document_controller import router as doc_router  # noqa: E402


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


@app.get("/health")
def health():
    return {"status": "ok"}
