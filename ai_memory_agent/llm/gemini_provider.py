import os
import json
import logging
from typing import Dict, Any, Optional

from ai_memory_agent.config import settings
from ai_memory_agent.llm.base import BaseLLMProvider
from ai_memory_agent.llm.expert_engine import SecurityExpertEngine

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini API Provider using google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or settings.GEMINI_MODEL
        self.fallback = SecurityExpertEngine()
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Initialized Gemini Client with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai client ({e}); using fallback expert engine.")
                self.client = None

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.client:
            return self.fallback.generate(prompt, system_prompt)
        try:
            full_prompt = f"System: {system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
            )
            return response.text
        except Exception as e:
            logger.warning(f"Gemini generate_content failed ({e}); invoking fallback.")
            return self.fallback.generate(prompt, system_prompt)

    def analyze_incident(
        self,
        incident_data: Dict[str, Any],
        historical_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Always run through the expert engine base structure, enhanced by Gemini if available
        base_result = self.fallback.analyze_incident(incident_data, historical_context)
        if not self.client:
            return base_result

        try:
            prompt = (
                f"You are a Principal Security Operations & Memory Agent. Analyze this incident:\n"
                f"{json.dumps(incident_data, indent=2)}\n\n"
                f"Hindsight Historical Memory Context:\n{historical_context or 'No prior incidents recorded.'}\n\n"
                f"Provide concise, high-impact security analysis, root cause details, and post-mortem notes."
            )
            llm_text = self.generate(prompt)
            if llm_text:
                base_result["llm_insights"] = llm_text
        except Exception as e:
            logger.warning(f"Gemini incident analysis augmentation failed: {e}")

        return base_result

    def generate_audit_response(
        self,
        audit_query: str,
        historical_findings: list,
        evidence_items: list,
    ) -> Dict[str, Any]:
        return self.fallback.generate_audit_response(audit_query, historical_findings, evidence_items)
