from typing import Optional
from ai_memory_agent.memory.hindsight_adapter import HindsightAdapter
from ai_memory_agent.llm.base import BaseLLMProvider
from ai_memory_agent.llm.factory import get_llm_provider


class BaseAgent:
    """Base class providing shared Hindsight Memory and LLM reasoning services."""

    def __init__(
        self,
        memory_adapter: Optional[HindsightAdapter] = None,
        llm_provider: Optional[BaseLLMProvider] = None,
    ):
        self.memory = memory_adapter or HindsightAdapter()
        self.llm = llm_provider or get_llm_provider()
