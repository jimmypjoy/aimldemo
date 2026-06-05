import os

from mcp.server.fastmcp import FastMCP

from resources.document_qa_guidance import DOCUMENT_QA_GUIDANCE
from tools.document_qa_tool import build_qa_response

mcp = FastMCP(
    name="document-qa-mcp",
    host=os.getenv("MCP_HOST", "127.0.0.1"),
    port=int(os.getenv("MCP_PORT", "3001")),
)


@mcp.resource("document-qa://guidance")
def document_qa_guidance() -> str:
    """General-purpose guidance for answering questions from ingested PDF documents."""
    return DOCUMENT_QA_GUIDANCE


@mcp.tool()
def answer_document_question(document_text: str, question: str) -> str:
    """
    Provides step-by-step guidance and an output schema for answering any user
    question from the supplied document chunks.

    Supports: specific factual questions, page summaries, comparisons,
    explanations, and list extraction.

    Args:
        document_text: Concatenated text of the retrieved document chunks,
                       including page numbers where available.
        question: The user's original question exactly as asked.

    Returns:
        JSON string containing Q&A guidance, output schema, and instructions.
    """
    return build_qa_response(document_text, question)
