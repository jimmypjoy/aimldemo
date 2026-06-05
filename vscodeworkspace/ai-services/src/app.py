import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Deferred import: must run after load_dotenv() and logging.basicConfig() so that
# module-level singletons (OpenAI client, loggers) initialise with env vars and
# logging already configured.
from controllers.llm_inference_controller import router as llm_router  # noqa: E402

app = FastAPI(title="AI Services", version="1.0.0")
app.include_router(llm_router)

logger.info("FastAPI app initialised | OPENAI_API_KEY configured=%s",
            bool(os.getenv("OPENAI_API_KEY")))


@app.get("/health")
def health():
    return {"status": "ok"}
