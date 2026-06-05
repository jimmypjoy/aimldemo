import json

from resources.credit_risk_guidance import CREDIT_RISK_GUIDANCE

EXTRACTION_SCHEMA = {
    "credit_risk_summary": {
        "bullet_1_exposure": None,
        "bullet_2_portfolio_composition": None,
        "bullet_3_risk_management": None,
        "bullet_4_key_risk_drivers": None,
        "bullet_5_overall_assessment": None,
    },
    "extraction_metadata": {
        "document_section": None,
        "confidence_score": None,
        "extraction_notes": None,
    },
}


def build_extraction_response(document_text: str) -> str:
    """
    Returns the extraction guidance and expected output schema for the agent.
    The agent uses this to produce a 5-bullet credit risk summary from the document.
    """
    word_count = len(document_text.split()) if document_text else 0

    response = {
        "guidance": CREDIT_RISK_GUIDANCE,
        "output_schema": EXTRACTION_SCHEMA,
        "instructions": (
            "Follow the guidance steps above to extract a credit risk summary from the "
            "provided document chunks. Populate the output_schema with exactly 5 bullet "
            "points as described. Set any field to null if the information is not present "
            "in the document. Do not infer or estimate values not explicitly stated."
        ),
        "document_stats": {
            "word_count": word_count,
            "document_preview": document_text[:500] if document_text else "",
        },
    }

    return json.dumps(response, indent=2)
