from enum import Enum


class LLMModel(Enum):
    # OpenAI GPT-4o series
    GPT_4O = ("GPT", "gpt-4o")
    GPT_4O_MINI = ("GPT", "gpt-4o-mini")

    # OpenAI GPT-4.1 series
    GPT_4_1 = ("GPT", "gpt-4.1")
    GPT_4_1_MINI = ("GPT", "gpt-4.1-mini")
    GPT_4_1_NANO = ("GPT", "gpt-4.1-nano")

    # OpenAI GPT-5 series
    GPT_5 = ("GPT", "gpt-5")
    GPT_5_MINI = ("GPT", "gpt-5-mini")

    # Google Gemini 2.5 series
    GEMINI_2_5_PRO = ("GEMINI", "gemini-2.5-pro")
    GEMINI_2_5_FLASH = ("GEMINI", "gemini-2.5-flash")

    # Google Gemini 2.0 series
    GEMINI_2_0_FLASH = ("GEMINI", "gemini-2.0-flash")

    def __init__(self, family: str, model_name: str):
        self.family = family
        self.model_name = model_name
