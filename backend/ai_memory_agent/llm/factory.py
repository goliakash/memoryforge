import os
from ai_memory_agent.config import settings
from ai_memory_agent.llm.base import BaseLLMProvider
from ai_memory_agent.llm.expert_engine import SecurityExpertEngine
from ai_memory_agent.llm.gemini_provider import GeminiProvider
from ai_memory_agent.llm.openai_provider import OpenAIProvider


def get_llm_provider() -> BaseLLMProvider:
    provider_pref = settings.LLM_PROVIDER.lower().strip()

    if provider_pref == "gemini" or (provider_pref == "auto" and (settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"))):
        return GeminiProvider()

    if provider_pref == "openai" or (provider_pref == "auto" and (settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"))):
        return OpenAIProvider()

    # Default to built-in Security Expert Engine (fully local, deterministic, and instant)
    return SecurityExpertEngine()
