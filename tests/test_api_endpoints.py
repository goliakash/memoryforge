import pytest
from starlette.testclient import TestClient
from ai_memory_agent.api.server import app

client = TestClient(app)


def test_root_and_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "documentation" in resp.json()

    health_resp = client.get("/api/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "healthy"


def test_api_investigate_and_audit():
    # Ingest incident
    payload = {
        "incident_id": "INC-TEST-01",
        "title": "Public Cloud Storage Exposure",
        "description": "Bucket public read test",
        "severity": "HIGH",
        "affected_asset": "test-data-bucket",
        "asset_type": "cloud_storage",
        "evidence": "ACL is public",
    }
    inv_resp = client.post("/api/incidents/investigate", json=payload)
    assert inv_resp.status_code == 200
    data = inv_resp.json()
    assert data["incident"]["incident_id"] == "INC-TEST-01"
    assert data["root_cause"]["category"] == "Access Policy Misconfiguration"

    # List incidents
    list_resp = client.get("/api/incidents")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    # Query audit
    audit_payload = {
        "control": "Access Control",
        "request": "Show me access control findings and evidence",
    }
    audit_resp = client.post("/api/audit/query", json=audit_payload)
    assert audit_resp.status_code == 200
    audit_data = audit_resp.json()
    assert len(audit_data["historical_findings"]) >= 1

    # Recall memory
    recall_resp = client.get("/api/memory/recall?query=storage+bucket")
    assert recall_resp.status_code == 200
    assert len(recall_resp.json()) >= 1


def test_api_run_demo_story():
    resp = client.post("/api/demo/run-story")
    assert resp.status_code == 200
    story = resp.json()
    assert story["status"] == "SUCCESS"
    assert len(story["steps"]) == 10
