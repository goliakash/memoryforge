from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ai_memory_agent.models.incident import Incident, IncidentIngestRequest
from ai_memory_agent.models.investigation import InvestigationResult
from ai_memory_agent.models.audit import AuditRequest, AuditResponse
from ai_memory_agent.models.memory_records import MemoryNetworkType, RecallItem, ReflectResult
from ai_memory_agent.agents.orchestrator import SecurityMemoryOrchestrator

router = APIRouter(prefix="/api", tags=["Security Memory Agent"])

# Singleton orchestrator instance
orchestrator = SecurityMemoryOrchestrator()


@router.post("/incidents/investigate", response_model=InvestigationResult, summary="Investigate and Retain Incident")
def investigate_incident(req: IncidentIngestRequest):
    """
    Ingests a security incident, queries Hindsight memory for prior incidents,
    conducts AI investigation (RCA, MITRE mapping, post-mortem), maps controls,
    fingerprints evidence, and retains knowledge in Hindsight organizational memory.
    """
    try:
        incident = Incident(
            incident_id=req.incident_id,
            title=req.title,
            description=req.description,
            severity=req.severity,
            affected_asset=req.affected_asset,
            asset_type=req.asset_type or "cloud_storage",
            evidence=req.evidence,
            tags=req.tags or [],
        )
        result = orchestrator.investigate_and_remember(incident)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Incident investigation failed: {str(e)}")


@router.get("/incidents", response_model=List[Dict[str, Any]], summary="List Processed Incidents")
def list_incidents():
    """Returns a summary list of all investigated security incidents."""
    return [
        {
            "incident_id": inv.incident.incident_id,
            "title": inv.incident.title,
            "severity": inv.incident.severity.value,
            "affected_asset": inv.incident.affected_asset,
            "root_cause_category": inv.root_cause.category,
            "is_recurring_issue": inv.is_recurring_issue,
            "recurrence_count": inv.recurrence_count,
            "recalled_incident": inv.recalled_prior_incident.recalled_incident_id if inv.recalled_prior_incident else None,
            "investigated_at": inv.investigated_at.isoformat(),
        }
        for inv in orchestrator.investigations_registry.values()
    ]


@router.get("/incidents/{incident_id}", response_model=InvestigationResult, summary="Get Incident Details")
def get_incident(incident_id: str):
    """Retrieves full investigation result, RCA, post-mortem, and evidence for an incident."""
    res = orchestrator.investigations_registry.get(incident_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")
    return res


@router.post("/audit/query", response_model=AuditResponse, summary="Submit Auditor Inquiry")
def query_audit(req: AuditRequest):
    """
    Handles external auditor inquiries against Hindsight organizational memory.
    Returns matched controls, historical findings, remediation statuses, and evidence hashes.
    """
    try:
        return orchestrator.handle_audit_request(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit query failed: {str(e)}")


@router.get("/memory/recall", response_model=List[RecallItem], summary="Query Hindsight Memory Directly")
def memory_recall(
    query: str = Query(..., description="Semantic search query"),
    network: Optional[MemoryNetworkType] = Query(None, description="Optional network filter: world, experience, observation, opinion"),
    limit: int = Query(5, ge=1, le=20),
    min_score: float = Query(0.20, ge=0.0, le=1.0, description="Minimum relevance threshold"),
):
    """Directly queries the Hindsight Memory bank using hybrid semantic search."""
    return orchestrator.memory.recall(query=query, limit=limit, network=network, min_score=min_score)


@router.get("/memory/reflect", response_model=ReflectResult, summary="Reflect on Organizational Memory Topic")
def memory_reflect(topic: str = Query("Access Control", description="Topic or control area to reflect upon")):
    """Synthesizes cross-incident observations, recurring patterns, and risk posture."""
    return orchestrator.memory.reflect(topic=topic)


@router.get("/memory/networks", summary="Inspect Memory Networks Summary")
def memory_networks():
    """Returns memory unit counts and distribution across World, Experience, Observation, and Opinion networks."""
    return orchestrator.memory.get_networks_summary()


@router.get("/memory/timeline", summary="Chronological Organizational Memory Timeline")
def memory_timeline():
    """Returns chronological stream of all security knowledge retained in Hindsight."""
    return orchestrator.memory.get_timeline()


@router.post("/demo/run-story", summary="Execute Full 10-Step Continuous Demo Story")
def run_demo_story():
    """
    Executes the complete 10-step demo story demonstrating:
    Incident #1024 -> AI Investigation -> Retain in Hindsight ->
    Incident #1038 -> Hindsight Recall -> Knowledge Reuse ->
    Auditor Query -> Evidence Retrieval.
    """
    try:
        story_result = orchestrator.run_demo_story()
        return story_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo story execution failed: {str(e)}")


@router.get("/health", summary="System Health and Status")
def health():
    return {
        "status": "healthy",
        "service": "AI Security Operations & Compliance Memory Agent",
        "memory_backend": "Hindsight Memory System",
        "networks_status": orchestrator.memory.get_networks_summary(),
        "llm_engine": orchestrator.llm.__class__.__name__,
    }
