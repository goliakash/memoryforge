import pytest
from ai_memory_agent.agents.investigation_agent import SecurityInvestigationAgent
from ai_memory_agent.models.incident import Incident, IncidentSeverity


def test_investigation_agent_rca_and_post_mortem():
    agent = SecurityInvestigationAgent()
    agent.memory.clear()

    incident = Incident(
        incident_id="INC-1024",
        title="Public Cloud Storage Exposure",
        description="A production storage bucket was discovered with public read access.",
        severity=IncidentSeverity.HIGH,
        affected_asset="customer-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access via permissive ACL and wildcard Principal.",
    )

    inv_data = agent.investigate(incident)

    assert inv_data["root_cause"].category == "Access Policy Misconfiguration"
    assert inv_data["root_cause"].confidence >= 0.90
    assert len(inv_data["mitre_techniques"]) >= 1
    assert inv_data["mitre_techniques"][0].technique_id == "T1530"
    assert inv_data["post_mortem"].incident_id == "INC-1024"
    assert len(inv_data["post_mortem"].timeline) >= 2
    assert inv_data["is_recurring_issue"] is False
