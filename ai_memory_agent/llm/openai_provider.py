import os
import json
import logging
from typing import Dict, Any, Optional

from ai_memory_agent.config import settings
from ai_memory_agent.llm.base import BaseLLMProvider
from ai_memory_agent.llm.expert_engine import SecurityExpertEngine

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API Provider."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name or settings.OPENAI_MODEL
        self.fallback = SecurityExpertEngine()
        self.client = None

        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI Client with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client ({e}); using fallback.")
                self.client = None

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.client:
            return self.fallback.generate(prompt, system_prompt)
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            resp = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.warning(f"OpenAI completion failed ({e}); invoking fallback.")
            return self.fallback.generate(prompt, system_prompt)

    def analyze_incident(
        self,
        incident_data: Dict[str, Any],
        historical_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        base_result = self.fallback.analyze_incident(incident_data, historical_context)
        if not self.client:
            return base_result
        try:
            prompt = (
                f"Incident Data:\n{json.dumps(incident_data, indent=2)}\n\n"
                f"Historical Memory Context:\n{historical_context or 'None'}\n\n"
                f"Synthesize advanced security assessment and post-mortem insights."
            )
            resp = self.generate(prompt)
            if resp:
                base_result["llm_insights"] = resp
        except Exception as e:
            logger.warning(f"OpenAI incident analysis failed: {e}")
        return base_result

    def generate_audit_response(
        self,
        audit_query: str,
        historical_findings: list,
        evidence_items: list,
    ) -> Dict[str, Any]:
        return self.fallback.generate_audit_response(audit_query, historical_findings, evidence_items)
