import pytest
from ai_memory_agent.agents.orchestrator import SecurityMemoryOrchestrator
from ai_memory_agent.models.incident import Incident, IncidentSeverity
from ai_memory_agent.models.audit import AuditRequest


def test_full_orchestrator_memory_loop():
    orchestrator = SecurityMemoryOrchestrator()
    orchestrator.memory.clear()

    # Step 1: Process Incident #1024
    inc1024 = Incident(
        incident_id="INC-1024",
        title="Public Cloud Storage Exposure",
        description="A production storage bucket was discovered with public read access.",
        severity=IncidentSeverity.HIGH,
        affected_asset="customer-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access via permissive ACL and wildcard Principal.",
    )
    res1024 = orchestrator.investigate_and_remember(inc1024)

    assert res1024.root_cause.category == "Access Policy Misconfiguration"
    assert res1024.is_recurring_issue is False
    assert res1024.recalled_prior_incident is None

    # Step 2: Process Incident #1038 (Similar incident)
    inc1038 = Incident(
        incident_id="INC-1038",
        title="Analytics Cloud Storage Bucket Public Exposure",
        description="Production analytics storage bucket discovered with unauthenticated public read permissions.",
        severity=IncidentSeverity.HIGH,
        affected_asset="analytics-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access: AWS Config rule failed.",
    )
    res1038 = orchestrator.investigate_and_remember(inc1038)

    # Validate Hindsight Recall
    assert res1038.recalled_prior_incident is not None
    assert res1038.recalled_prior_incident.recalled_incident_id == "INC-1024"
    assert res1038.recalled_prior_incident.relevance_score >= 0.35
    assert res1038.is_recurring_issue is True
    assert res1038.recurrence_count >= 2

    # Step 3: Auditor Request
    audit_req = AuditRequest(
        control="Access Control",
        request="Show me previous findings related to access control, their remediation status, and available evidence.",
    )
    audit_res = orchestrator.handle_audit_request(audit_req)

    assert len(audit_res.historical_findings) >= 2
    assert any(f.incident_id == "INC-1024" for f in audit_res.historical_findings)
    assert any(f.incident_id == "INC-1038" for f in audit_res.historical_findings)
    assert len(audit_res.evidence_items) >= 4
    assert audit_res.compliance_posture == "COMPLIANT_WITH_REMEDIATION_EVIDENCE"


def test_demo_story_method():
    orchestrator = SecurityMemoryOrchestrator()
    orchestrator.memory.clear()
    story = orchestrator.run_demo_story()
    assert story["status"] == "SUCCESS"
    assert len(story["steps"]) == 10
    assert story["inc1038_result"].is_recurring_issue is True
