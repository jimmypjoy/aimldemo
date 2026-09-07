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
    GPT_5_5 = ("GPT", "gpt-5.5")
    GPT_5_MINI = ("GPT", "gpt-5-mini")
    GPT_5_NANO = ("GPT", "gpt-5-nano")

    # OpenAI web-search-grounded series (for use with use_web_search=True)
    GPT_4O_SEARCH_PREVIEW = ("GPT", "gpt-4o-search-preview")
    GPT_4O_MINI_SEARCH_PREVIEW = ("GPT", "gpt-4o-mini-search-preview")
    GPT_5_SEARCH_API = ("GPT", "gpt-5-search-api")

    # Google Gemini 3.1 series
    GEMINI_3_1_PRO_PREVIEW = ("GEMINI", "gemini-3.1-pro-preview")

    # Google Gemini 2.5 series
    GEMINI_2_5_PRO = ("GEMINI", "gemini-2.5-pro")
    GEMINI_2_5_FLASH = ("GEMINI", "gemini-2.5-flash")

    # Google Gemini 2.0 series
    GEMINI_2_0_FLASH = ("GEMINI", "gemini-2.0-flash")
    GEMINI_2_0_FLASH_LITE = ("GEMINI", "gemini-2.0-flash-lite")

    # Google Gemini 1.5 series
    GEMINI_1_5_PRO = ("GEMINI", "gemini-1.5-pro")
    GEMINI_1_5_FLASH = ("GEMINI", "gemini-1.5-flash")

    def __init__(self, family: str, model_name: str):
        self.family = family
        self.model_name = model_name
