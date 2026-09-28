from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from ai_memory_agent.models.compliance import (
    ComplianceFramework,
    FindingStatus,
    SecurityControl,
    SecurityFinding,
    EvidenceItem,
)


class AuditRequest(BaseModel):
    control: str = Field(..., description="Target control or category, e.g. Access Control, CC6.1, PR.AC-4")
    framework: Optional[ComplianceFramework] = None
    request: str = Field(..., description="Auditor's query in natural language")
    requested_by: str = Field(default="External Compliance Auditor")
    timeframe: Optional[str] = Field(default="All Historical Periods")


class AuditFindingSummary(BaseModel):
    finding_id: str
    incident_id: str
    incident_title: str
    control_id: str
    control_name: str
    framework: str
    severity: str
    status: FindingStatus
    root_cause: str
    remediation_summary: List[str]
    evidence_count: int
    evidence_hashes: List[str]
    detected_at: datetime
    resolved_at: Optional[datetime] = None


class AuditResponse(BaseModel):
    request: AuditRequest
    matched_controls: List[SecurityControl]
    historical_findings: List[AuditFindingSummary]
    evidence_items: List[EvidenceItem]
    remediation_summary: Dict[str, Any]
    recurring_patterns_detected: List[str]
    compliance_posture: str
    executive_summary: str
    auditor_verification_notes: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
