import os
import sys
from pathlib import Path

# Add src to path so config is accessible when ADK loads this agent directly
_src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_src_dir))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent.parent / ".env")

import json
import logging

import requests as _requests

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import MCPToolset, SseConnectionParams

logger = logging.getLogger(__name__)

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:3001")
DOCUMENT_SERVICE_URL = os.getenv("DOCUMENT_SERVICE_URL", "http://127.0.0.1:8001")


# ── Document service tools ────────────────────────────────────────────────────

def search_document(query: str, file_name: str = "", top_k: int = 8) -> str:
    """
    Search the document store for chunks relevant to the query.
    Returns a JSON string with a list of chunks, each containing:
    chunk_text, page_start, file_name, similarity_score, chunk_sequence.

    Args:
        query: The search phrase derived from the user's question.
        file_name: Optional. Scope the search to a specific PDF file name.
                   Pass empty string to search across all documents.
        top_k: Number of chunks to retrieve (default 8).
    """
    payload: dict = {"query": query, "top_k": top_k}
    if file_name:
        payload["file_name"] = file_name

    logger.info("search_document | query=%.60s file_name=%s top_k=%d", query, file_name, top_k)
    try:
        resp = _requests.post(
            f"{DOCUMENT_SERVICE_URL}/api/v1/documents/query",
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        chunks = data.get("results", [])
        simplified = [
            {
                "page": c.get("page_start"),
                "file_name": c.get("file_name"),
                "score": c.get("similarity_score"),
                "text": c.get("chunk_text"),
            }
            for c in chunks
        ]
        logger.info("search_document | returned %d chunks", len(simplified))
        return json.dumps({"chunks": simplified, "total": len(simplified)})
    except Exception as exc:
        logger.error("search_document failed | %s", exc)
        return json.dumps({"error": str(exc), "chunks": []})


def list_documents() -> str:
    """
    List all PDF documents that have been ingested into the document store.
    Returns a JSON string with file names, page counts, and ingestion status.
    """
    logger.info("list_documents called")
    try:
        resp = _requests.get(
            f"{DOCUMENT_SERVICE_URL}/api/v1/documents",
            timeout=10,
        )
        resp.raise_for_status()
        docs = resp.json()
        simplified = [
            {
                "file_name": d.get("file_name"),
                "page_count": d.get("page_count"),
                "status": d.get("ingestion_status"),
            }
            for d in docs
        ]
        logger.info("list_documents | returned %d documents", len(simplified))
        return json.dumps({"documents": simplified})
    except Exception as exc:
        logger.error("list_documents failed | %s", exc)
        return json.dumps({"error": str(exc), "documents": []})


# ── Agent ─────────────────────────────────────────────────────────────────────

root_agent = Agent(
    name="document_qa_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description=(
        "General-purpose document Q&A agent. Answers any question from ingested PDF "
        "documents with page-level citations."
    ),
    instruction=f"""
You are a helpful document assistant. Users ask questions about PDF documents ingested
into the document store. You have tools to search and list those documents.

AVAILABLE TOOLS:
- list_documents() — lists all ingested PDFs with their file names and page counts.
- search_document(query, file_name, top_k) — searches document content and returns
  matching chunks with page numbers. Always call this to retrieve content before answering.
- answer_document_question(document_text, question) — MCP tool that provides structured
  Q&A guidance. Call it with the retrieved chunk text and the user's question.

WORKFLOW for every user question:
1. If you do not know what documents are available, call list_documents() first.
2. Identify the file the user is asking about (from context or by asking).
3. Call search_document() with a query phrase that captures the user's intent.
   - For specific values/numbers: query the exact metric (e.g. "Markets division average loans")
   - For page summaries: query "page <N> <topic>" and use top_k=10
   - For comparisons: query the metric with the time period (e.g. "average loans 2024 2023")
   - For general questions: query the key topic with top_k=5
4. From the returned chunks, extract the answer. Each chunk contains:
   - text: the document text
   - page: the page number (use this for citations)
   - file_name: source document
   - score: relevance score (higher = more relevant)
5. Optionally call answer_document_question() passing the chunks as document_text
   and the user's question to get structured guidance.
6. Formulate your final answer in the format the user requested.

PAGE CITATION RULES — mandatory:
- Every specific fact, figure, or statement MUST end with (p. N).
- Example: "Average loans for Markets increased 8% year-over-year (p. 68)."
- If a finding comes from multiple pages: (p. 68, 69).
- If page is null in the chunk: write (page unknown).
- End every response with a "Sources" section listing all pages cited.

CONTENT RULES:
- Only use information from the retrieved chunks. Never use external knowledge.
- If search_document returns no relevant chunks, say clearly:
  "I could not find that information in the ingested document."
- Do not estimate or infer values not explicitly stated in the chunk text.
- For page summaries: retrieve chunks filtered to that page and summarise all content found.
""",
    tools=[
        search_document,
        list_documents,
        MCPToolset(
            connection_params=SseConnectionParams(url=f"{MCP_SERVER_URL}/sse")
        ),
    ],
)
