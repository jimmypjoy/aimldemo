from typing import Optional

from pydantic import BaseModel


class IngestRequest(BaseModel):
    file_name: str
    document_type: Optional[str] = "PDF"
    source_system: Optional[str] = "local"
    metadata: Optional[dict] = None
