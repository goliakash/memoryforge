import pytest
from ai_memory_agent.agents.audit_agent import AuditAgent
from ai_memory_agent.models.audit import AuditRequest
from ai_memory_agent.models.compliance import (
    SecurityFinding,
    EvidenceItem,
    FindingSeverity,
    FindingStatus,
    ComplianceFramework,
)


def test_audit_agent_query():
    agent = AuditAgent()

    # Prepopulate a test finding
    finding = SecurityFinding(
        finding_id="FIND-1024-CC6-1",
        incident_id="INC-1024",
        control_id="SOC2-CC6.1",
        control_name="Logical Access Security",
        framework=ComplianceFramework.SOC2,
        title="Non-compliance with SOC2-CC6.1 on customer-data-bucket",
        description="Public access violation",
        severity=FindingSeverity.HIGH,
        status=FindingStatus.REMEDIATED,
        root_cause_summary="Incorrect access policy",
    )

    evidence = EvidenceItem(
        evidence_id="EVD-1024-SCAN",
        incident_id="INC-1024",
        evidence_type="configuration_scan",
        description="Public access scan alert",
        raw_data="Alert data",
        hash_digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )

    req = AuditRequest(
        control="Access Control",
        request="Show historical access-control findings, remediation status, and available evidence.",
    )

    resp = agent.process_audit_request(
        audit_request=req,
        known_findings=[finding],
        known_evidence=[evidence],
    )

    assert len(resp.historical_findings) >= 1
    assert resp.historical_findings[0].incident_id == "INC-1024"
    assert resp.historical_findings[0].status == FindingStatus.REMEDIATED
    assert resp.compliance_posture == "COMPLIANT_WITH_REMEDIATION_EVIDENCE"
    assert "100.0%" in resp.executive_summary
