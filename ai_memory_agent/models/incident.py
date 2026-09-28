from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class IncidentSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    CONTAINED = "CONTAINED"
    REMEDIATED = "REMEDIATED"
    CLOSED = "CLOSED"


class RawEvidence(BaseModel):
    source: str = Field(..., description="Source of evidence (e.g. AWS GuardDuty, CloudTrail, Trivy, Config)")
    raw_payload: str = Field(..., description="Raw finding text or log message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    evidence_type: str = Field(default="configuration_scan", description="Type of evidence: config, log, network, code")


class Incident(BaseModel):
    incident_id: str = Field(..., description="Unique incident identifier, e.g. INC-1024")
    title: str = Field(..., description="Short title describing incident, e.g. Public Cloud Storage Exposure")
    description: str = Field(..., description="Full text description of the security event")
    severity: IncidentSeverity = Field(default=IncidentSeverity.HIGH)
    affected_asset: str = Field(..., description="Resource or system impacted, e.g. customer-data-bucket")
    asset_type: str = Field(default="cloud_storage", description="Category of asset, e.g. cloud_storage, iam_role, k8s_pod")
    evidence: str = Field(..., description="Primary evidence text or detection alert")
    raw_evidence_items: List[RawEvidence] = Field(default_factory=list)
    status: IncidentStatus = Field(default=IncidentStatus.DETECTED)
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IncidentIngestRequest(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity = IncidentSeverity.HIGH
    affected_asset: str
    asset_type: Optional[str] = "cloud_storage"
    evidence: str
    tags: Optional[List[str]] = None
