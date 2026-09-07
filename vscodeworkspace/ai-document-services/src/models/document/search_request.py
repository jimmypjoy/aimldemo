from typing import Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    file_name: Optional[str] = None
    top_k: int = 5
    llm_model: Optional[str] = "gemini-3.1-pro-preview"
