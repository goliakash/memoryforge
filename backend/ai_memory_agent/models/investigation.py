from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from ai_memory_agent.models.incident import Incident
from ai_memory_agent.models.compliance import SecurityControl, SecurityFinding, RemediationStep, EvidenceItem


class RootCause(BaseModel):
    category: str = Field(..., description="E.g. Access Policy Misconfiguration, Unpatched CVE, Weak Credentials")
    summary: str = Field(..., description="Concise explanation of the underlying failure")
    technical_details: str = Field(..., description="In-depth technical breakdown of the flaw")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    contributing_factors: List[str] = Field(default_factory=list)


class MITRETechnique(BaseModel):
    technique_id: str = Field(..., description="e.g. T1530")
    name: str = Field(..., description="Data from Cloud Storage")
    tactic: str = Field(..., description="Collection / Initial Access")


class PostMortem(BaseModel):
    post_mortem_id: str
    incident_id: str
    incident_title: str
    executive_summary: str
    timeline: List[str] = Field(default_factory=list)
    root_cause: str
    impact_blast_radius: str
    lessons_learned: List[str] = Field(default_factory=list)
    preventive_actions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecalledMemoryContext(BaseModel):
    recalled_incident_id: str
    recalled_title: str
    relevance_score: float
    recalled_root_cause: str
    recalled_remediations: List[str]
    recalled_controls: List[str]
    match_reason: str


class InvestigationResult(BaseModel):
    incident: Incident
    root_cause: RootCause
    mitre_techniques: List[MITRETechnique] = Field(default_factory=list)
    security_controls: List[SecurityControl] = Field(default_factory=list)
    findings: List[SecurityFinding] = Field(default_factory=list)
    remediation_steps: List[RemediationStep] = Field(default_factory=list)
    evidence_collected: List[EvidenceItem] = Field(default_factory=list)
    post_mortem: PostMortem
    recalled_prior_incident: Optional[RecalledMemoryContext] = None
    is_recurring_issue: bool = False
    recurrence_count: int = 1
    recurrence_rationale: Optional[str] = None
    investigated_at: datetime = Field(default_factory=datetime.utcnow)
    execution_time_ms: float = 0.0
