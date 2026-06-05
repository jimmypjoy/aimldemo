import json

from resources.document_qa_guidance import DOCUMENT_QA_GUIDANCE

OUTPUT_SCHEMA = {
    "answer": None,
    "answer_format": None,
    "page_citations": [],
    "confidence": None,
    "notes": None,
}


def build_qa_response(document_text: str, question: str) -> str:
    """
    Returns Q&A guidance and output schema for the agent to answer
    a user question from the supplied document chunks.
    """
    word_count = len(document_text.split()) if document_text else 0

    response = {
        "guidance": DOCUMENT_QA_GUIDANCE,
        "output_schema": OUTPUT_SCHEMA,
        "question": question,
        "instructions": (
            "Use the guidance above to answer the question from the provided document chunks. "
            "Respond in exactly the format the user requested. "
            "Every fact or figure MUST include a (p. N) page citation. "
            "Populate the output_schema: set answer to your response, "
            "page_citations to a list of page numbers used, "
            "confidence to high/medium/low based on how clearly the answer appears in the chunks, "
            "and notes to any caveats or missing information."
        ),
        "document_stats": {
            "word_count": word_count,
            "document_preview": document_text[:300] if document_text else "",
        },
    }

    return json.dumps(response, indent=2)
