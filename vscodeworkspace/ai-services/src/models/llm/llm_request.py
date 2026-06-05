from typing import Optional

from pydantic import BaseModel, field_validator

from llm.enums.llm_enum import LLMModel


class LLMRequest(BaseModel):
    query: str
    prompt: Optional[str] = ""
    llm_model: LLMModel
    user_role: Optional[str] = "user"

    @field_validator("llm_model", mode="before")
    @classmethod
    def parse_llm_model(cls, v):
        if isinstance(v, LLMModel):
            return v
        if isinstance(v, str):
            try:
                return LLMModel[v]          # match by key e.g. "GPT_4_1"
            except KeyError:
                pass
            for model in LLMModel:
                if model.model_name == v:   # match by value e.g. "gpt-4.1"
                    return model
        raise ValueError(f"Invalid LLM model: {v!r}")
