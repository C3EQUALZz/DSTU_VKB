from enum import StrEnum


class LLMProviderType(StrEnum):
    """Enumeration of supported LLM providers."""

    MIMO_V2_FLASH = "xiaomi/mimo-v2-flash:free"
    MISTRAL_DEVSTRAL_2512 = "mistralai/devstral-2512:free"
    NVIDIA_NEMOTRON_3 = "nvidia/nemotron-3-nano-30b-a3b:free"
    MISTRAL_DEVSTRAL_2_2512 = "mistralai/devstral-2512:free"
    NEX_AGI_DEEPSEEK_V_3_1 = "nex-agi/deepseek-v3.1-nex-n1:free"
    ARCEE_AI_TRINITY_MINI = "arcee-ai/trinity-mini:free"
    NVIDIA_NEMOTRON_NANO_9B_V2 = "nvidia/nemotron-nano-9b-v2:free"
    OPEN_AI_GPT_OSS_120B = "openai/gpt-oss-120b:free"
    QWEN_3_CODER = "qwen/qwen3-coder:free"
