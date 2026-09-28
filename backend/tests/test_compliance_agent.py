import pytest
from ai_memory_agent.agents.compliance_agent import ComplianceAgent
from ai_memory_agent.models.incident import Incident, IncidentSeverity
from ai_memory_agent.models.investigation import RootCause


def test_compliance_control_mapping_and_evidence():
    agent = ComplianceAgent()

    incident = Incident(
        incident_id="INC-1024",
        title="Public Cloud Storage Exposure",
        description="A production storage bucket was discovered with public read access.",
        severity=IncidentSeverity.HIGH,
        affected_asset="customer-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access.",
    )

    root_cause = RootCause(
        category="Access Policy Misconfiguration",
        summary="Permissive bucket policy allowed public read access.",
        technical_details="Wildcard Principal * in S3 bucket policy.",
    )

    # 1. Map controls
    controls = agent.map_security_controls(incident, root_cause)
    assert len(controls) >= 2
    control_ids = [c.control_id for c in controls]
    assert "SOC2-CC6.1" in control_ids
    assert "NIST-PR.AC-04" in control_ids

    # 2. Remediation plan
    rems = agent.generate_remediation_plan(incident, root_cause)
    assert len(rems) == 4
    assert "public-access-block" in rems[0].command_or_config

    # 3. Evidence fingerprinting
    evidence = agent.organize_and_fingerprint_evidence(incident, root_cause, rems)
    assert len(evidence) == 3
    for ev in evidence:
        assert len(ev.hash_digest) == 64  # SHA-256 hex digest length

    # 4. Findings creation
    findings = agent.create_findings(incident, root_cause, controls, rems, evidence)
    assert len(findings) == len(controls)
