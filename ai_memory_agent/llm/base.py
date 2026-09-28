from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMProvider(ABC):
    """Abstract interface for LLM reasoning engines."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response given a user prompt and optional system prompt."""
        pass

    @abstractmethod
    def analyze_incident(
        self,
        incident_data: Dict[str, Any],
        historical_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform security incident investigation and root cause analysis."""
        pass

    @abstractmethod
    def generate_audit_response(
        self,
        audit_query: str,
        historical_findings: list,
        evidence_items: list,
    ) -> Dict[str, Any]:
        """Generate audit report and compliance assessment."""
        pass
