import logging

from openai import AsyncOpenAI

from config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
_client = AsyncOpenAI()

_BATCH_SIZE = 100  # OpenAI allows up to 2048 inputs; 100 is safe for large text chunks


async def get_embedding(text: str) -> list[float]:
    """Generate a single embedding vector for the given text."""
    response = await _client.embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    return response.data[0].embedding


async def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts.
    Sends requests in batches to stay within API limits.
    """
    if not texts:
        return []

    all_embeddings: list[list[float]] = []

    for batch_start in range(0, len(texts), _BATCH_SIZE):
        batch = texts[batch_start: batch_start + _BATCH_SIZE]
        logger.info("Embedding batch %d-%d of %d",
                    batch_start + 1, batch_start + len(batch), len(texts))
        response = await _client.embeddings.create(
            model=settings.embedding_model,
            input=batch,
        )
        # Sort by index to guarantee order matches input
        sorted_data = sorted(response.data, key=lambda x: x.index)
        all_embeddings.extend(item.embedding for item in sorted_data)

    return all_embeddings
