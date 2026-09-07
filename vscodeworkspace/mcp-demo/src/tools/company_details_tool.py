from pathlib import Path

import pandas as pd

_COMPANY_DETAILS_PATH = Path(__file__).resolve().parent.parent / "resources" / "company_details.xlsx"


def get_company_details(company_name: str, company_details_key: str) -> str:
    """
    Look up a specific detail about a company from the internal company
    reference sheet.

    Args:
        company_name: The company name to look up (e.g. "Citi", "Walmart").
        company_details_key: The column whose value should be returned for
                              that company (e.g. "analyst_name",
                              "internal_rating", "next_review_date").

    Returns:
        The value found for that company and key, or a message explaining
        why nothing was found.
    """
    df = pd.read_excel(_COMPANY_DETAILS_PATH)

    if company_details_key not in df.columns:
        available = ", ".join(df.columns)
        return f"Unknown company_details_key '{company_details_key}'. Available keys: {available}"

    match = df[df["company_name"].str.strip().str.lower() == company_name.strip().lower()]
    if match.empty:
        return f"No company details found for '{company_name}'."

    value = match.iloc[0][company_details_key]
    if pd.isna(value):
        return f"No value set for '{company_details_key}' on '{company_name}'."

    return str(value)
