from typing import Optional

from pydantic import BaseModel, field_serializer

from llm.enums.llm_enum import LLMModel


class LLMResponse(BaseModel):
    llm_response: str
    llm_model: LLMModel
    response_time: float
    success: bool
    exception_message: Optional[str] = None

    @field_serializer("llm_model")
    def serialize_llm_model(self, value: LLMModel) -> str:
        return value.model_name
