from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ComplianceFramework(str, Enum):
    SOC2 = "SOC2_Type_II"
    NIST_CSF = "NIST_CSF_2.0"
    ISO27001 = "ISO_IEC_27001"
    CIS_CONTROLS = "CIS_Controls_v8"
    PCI_DSS = "PCI_DSS_v4.0"


class FindingSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    REMEDIATED = "REMEDIATED"
    VERIFIED = "VERIFIED"


class SecurityControl(BaseModel):
    control_id: str = Field(..., description="Unique control ID, e.g. SOC2-CC6.1 or NIST-PR.AC-4")
    framework: ComplianceFramework
    name: str = Field(..., description="Control title, e.g. Logical Access Security")
    category: str = Field(default="Access Control", description="Category e.g. Access Control, Data Protection")
    description: str = Field(..., description="Formal description of the control requirement")
    remediation_guidance: Optional[str] = None


class RemediationStatus(str, Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


class RemediationStep(BaseModel):
    step_id: str
    action: str = Field(..., description="Specific action, e.g. Remove public bucket read access")
    target_asset: str
    priority: int = Field(default=1, description="1 is highest priority containment")
    status: RemediationStatus = Field(default=RemediationStatus.PENDING)
    command_or_config: Optional[str] = None
    verification_criteria: str = Field(..., description="How to verify the fix works")
    executed_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None


class EvidenceItem(BaseModel):
    evidence_id: str = Field(..., description="Unique ID for the evidence artifact, e.g. EVD-1024-01")
    incident_id: str
    finding_id: Optional[str] = None
    evidence_type: str = Field(..., description="config_snapshot, log_trace, scan_finding, policy_document")
    description: str
    raw_data: str
    source: str = "Automated Security Agent"
    hash_digest: str = Field(..., description="SHA-256 fingerprint for integrity and audit readiness")
    collected_at: datetime = Field(default_factory=datetime.utcnow)


class SecurityFinding(BaseModel):
    finding_id: str = Field(..., description="Unique finding ID, e.g. FIND-1024-AC")
    incident_id: str
    control_id: str
    control_name: str
    framework: ComplianceFramework
    title: str
    description: str
    severity: FindingSeverity
    status: FindingStatus = FindingStatus.OPEN
    root_cause_summary: str
    remediation_steps: List[RemediationStep] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
