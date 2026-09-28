from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MemoryNetworkType(str, Enum):
    WORLD = "world"             # Objective environment facts (assets, controls, baselines)
    EXPERIENCE = "experience"   # Incident history, investigations, containment actions
    OBSERVATION = "observation" # Synthesized patterns across multiple incidents (e.g. repeated failure modes)
    OPINION = "opinion"         # Evolving beliefs with confidence scores (e.g. control degradation risk)


class MemoryUnit(BaseModel):
    id: str = Field(..., description="Unique memory unit ID")
    bank_id: str = Field(default="secops-org-memory")
    network_type: MemoryNetworkType
    content: str = Field(..., description="The semantic memory representation")
    entities: List[str] = Field(default_factory=list, description="Extracted entities, e.g. ['INC-1024', 'Access Control']")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecallQuery(BaseModel):
    query: str
    bank_id: str = Field(default="secops-org-memory")
    network: Optional[MemoryNetworkType] = None
    limit: int = 5
    min_score: float = 0.3


class RecallItem(BaseModel):
    memory_unit: MemoryUnit
    score: float = Field(..., description="Relevance / similarity score (0.0 to 1.0)")
    match_reason: str = Field(default="Semantic and lexical match")


class ReflectResult(BaseModel):
    topic: str
    synthesis: str
    recurring_patterns: List[str] = Field(default_factory=list)
    at_risk_controls: List[str] = Field(default_factory=list)
    recommended_policy_changes: List[str] = Field(default_factory=list)
    confidence: float = 0.90
    generated_at: datetime = Field(default_factory=datetime.utcnow)
