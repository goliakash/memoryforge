import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ai_memory_agent.memory.hindsight_adapter import HindsightAdapter
from ai_memory_agent.llm.base import BaseLLMProvider
from ai_memory_agent.llm.factory import get_llm_provider
from ai_memory_agent.agents.investigation_agent import SecurityInvestigationAgent
from ai_memory_agent.agents.compliance_agent import ComplianceAgent
from ai_memory_agent.agents.audit_agent import AuditAgent
from ai_memory_agent.models.incident import Incident, IncidentSeverity
from ai_memory_agent.models.investigation import InvestigationResult
from ai_memory_agent.models.compliance import SecurityFinding, EvidenceItem, RemediationStatus
from ai_memory_agent.models.audit import AuditRequest, AuditResponse
from ai_memory_agent.models.memory_records import MemoryNetworkType

logger = logging.getLogger(__name__)


class SecurityMemoryOrchestrator:
    """
    Central AI Orchestrator implementing the full Hindsight Memory Loop:
    Incident -> AI Investigation -> Root Cause -> Security Control ->
    Remediation -> Evidence -> Post-Mortem -> Hindsight Memory (Retain) ->
    Future Incident / Audit -> Hindsight Recall -> Better Investigation & Audit Readiness
    """

    def __init__(
        self,
        bank_id: Optional[str] = None,
        llm_provider: Optional[BaseLLMProvider] = None,
    ):
        self.memory = HindsightAdapter(bank_id=bank_id)
        self.llm = llm_provider or get_llm_provider()

        self.investigation_agent = SecurityInvestigationAgent(
            memory_adapter=self.memory, llm_provider=self.llm
        )
        self.compliance_agent = ComplianceAgent(
            memory_adapter=self.memory, llm_provider=self.llm
        )
        self.audit_agent = AuditAgent(
            memory_adapter=self.memory, llm_provider=self.llm
        )

        # In-memory registries of active findings and evidence for the session
        self.findings_registry: List[SecurityFinding] = []
        self.evidence_registry: List[EvidenceItem] = []
        self.investigations_registry: Dict[str, InvestigationResult] = {}

    def investigate_and_remember(self, incident: Incident) -> InvestigationResult:
        """
        Executes end-to-end investigation and stores knowledge in Hindsight memory.
        """
        # Step 1: Query Hindsight Memory for similar prior incidents
        recalled_context = self.investigation_agent.recall_prior_incidents(incident)

        # Step 2: AI Investigation Agent conducts root-cause analysis & post-mortem
        inv_data = self.investigation_agent.investigate(incident, recalled_context)

        root_cause = inv_data["root_cause"]
        mitre_techs = inv_data["mitre_techniques"]
        post_mortem = inv_data["post_mortem"]

        # Step 3: Compliance Agent maps Security Controls
        controls = self.compliance_agent.map_security_controls(incident, root_cause)

        # Step 4: Generate Remediation Plan (reuse historical remediations if available)
        reused_rems = recalled_context.recalled_remediations if recalled_context else None
        remediation_steps = self.compliance_agent.generate_remediation_plan(
            incident=incident,
            root_cause=root_cause,
            reused_remediations=reused_rems,
        )

        # Step 5: Organize and fingerprint Evidence (SHA-256)
        evidence_items = self.compliance_agent.organize_and_fingerprint_evidence(
            incident=incident,
            root_cause=root_cause,
            remediation_steps=remediation_steps,
        )
        self.evidence_registry.extend(evidence_items)

        # Step 6: Create Compliance Findings
        findings = self.compliance_agent.create_findings(
            incident=incident,
            root_cause=root_cause,
            controls=controls,
            remediation_steps=remediation_steps,
            evidence_items=evidence_items,
        )
        self.findings_registry.extend(findings)

        # Step 7: Store knowledge into Hindsight Memory (Retain)
        # 7a. Retain into Experience Network (Episodic incident investigation)
        exp_content = (
            f"Incident {incident.incident_id} [{incident.title}] on asset '{incident.affected_asset}'. "
            f"Severity: {incident.severity.value}. Root Cause: {root_cause.summary}. "
            f"Controls violated: {[c.control_id for c in controls]}. "
            f"Remediations executed: {[s.action for s in remediation_steps]}. "
            f"Evidence hashes: {[e.hash_digest[:16] for e in evidence_items]}."
        )
        self.memory.retain(
            content=exp_content,
            network_type=MemoryNetworkType.EXPERIENCE,
            entities=[incident.incident_id, incident.affected_asset, incident.asset_type, "Access Control"],
            tags=["incident", incident.severity.value.lower(), incident.asset_type],
            metadata={
                "incident_id": incident.incident_id,
                "title": incident.title,
                "asset": incident.affected_asset,
                "asset_type": incident.asset_type,
                "root_cause": root_cause.summary,
                "root_cause_category": root_cause.category,
                "controls": [c.control_id for c in controls],
                "remediations": [s.action for s in remediation_steps],
                "evidence_ids": [e.evidence_id for e in evidence_items],
            },
        )

        # Step 8: Build complete InvestigationResult
        result = InvestigationResult(
            incident=incident,
            root_cause=root_cause,
            mitre_techniques=mitre_techs,
            security_controls=controls,
            findings=findings,
            remediation_steps=remediation_steps,
            evidence_collected=evidence_items,
            post_mortem=post_mortem,
            recalled_prior_incident=recalled_context,
            is_recurring_issue=inv_data["is_recurring_issue"],
            recurrence_count=inv_data["recurrence_count"],
            recurrence_rationale=inv_data["recurrence_rationale"],
            investigated_at=datetime.utcnow(),
            execution_time_ms=inv_data["execution_time_ms"],
        )

        self.investigations_registry[incident.incident_id] = result
        return result

    def handle_audit_request(self, audit_request: AuditRequest) -> AuditResponse:
        """
        Executes audit inquiry against Hindsight organizational memory.
        """
        return self.audit_agent.process_audit_request(
            audit_request=audit_request,
            known_findings=self.findings_registry,
            known_evidence=self.evidence_registry,
        )

    def run_demo_story(self) -> Dict[str, Any]:
        """
        Executes the exact 10-step continuous demo story requested in the project prompt:
        1. Create Incident #1024
        2. AI investigates
        3. Root cause + control + remediation
        4. Store knowledge in Hindsight
        5. Create similar Incident #1038
        6. Agent recalls Incident #1024
        7. Agent uses previous knowledge
        8. Auditor asks for access-control findings
        9. Agent recalls historical findings
        10. Agent retrieves evidence + remediation status
        """
        logs = []

        def log_step(step_num: int, title: str, details: Any):
            logs.append({"step": step_num, "title": title, "details": details})

        # Step 1: Create Incident #1024
        inc1024 = Incident(
            incident_id="INC-1024",
            title="Public Cloud Storage Exposure",
            description="A production storage bucket was discovered with public read access.",
            severity=IncidentSeverity.HIGH,
            affected_asset="customer-data-bucket",
            asset_type="cloud_storage",
            evidence="Configuration scan detected public read access via permissive ACL and wildcard Principal in bucket policy.",
            detected_at=datetime.utcnow(),
        )
        log_step(1, "Create Incident #1024", {
            "incident_id": inc1024.incident_id,
            "title": inc1024.title,
            "asset": inc1024.affected_asset,
            "severity": inc1024.severity.value,
        })

        # Step 2-4: AI investigates, extracts RCA/Control/Remediation, and stores in Hindsight
        res1024 = self.investigate_and_remember(inc1024)
        log_step(2, "AI Investigates Incident #1024", {
            "root_cause": res1024.root_cause.summary,
            "confidence": res1024.root_cause.confidence,
        })
        log_step(3, "Root Cause + Control + Remediation + Evidence", {
            "controls": [f"{c.control_id}: {c.name}" for c in res1024.security_controls],
            "remediation_steps": [s.action for s in res1024.remediation_steps],
            "evidence_hashes": [f"{e.evidence_id} -> {e.hash_digest[:16]}..." for e in res1024.evidence_collected],
        })
        log_step(4, "Store Knowledge in Hindsight Memory", {
            "networks_updated": ["experience", "world", "observation"],
            "retained_unit_summary": f"Incident {inc1024.incident_id} root cause and remediation playbooks preserved in organizational memory.",
        })

        # Step 5: Create similar Incident #1038
        inc1038 = Incident(
            incident_id="INC-1038",
            title="Customer Analytics Cloud Storage Exposure",
            description="Production analytics storage bucket discovered with unauthenticated public read permissions.",
            severity=IncidentSeverity.HIGH,
            affected_asset="analytics-data-bucket",
            asset_type="cloud_storage",
            evidence="Configuration scan detected public access: s3-bucket-public-read-prohibited alert triggered.",
            detected_at=datetime.utcnow(),
        )
        log_step(5, "Create Similar Incident #1038", {
            "incident_id": inc1038.incident_id,
            "title": inc1038.title,
            "asset": inc1038.affected_asset,
        })

        # Step 6 & 7: AI recalls Incident #1024 and reuses previous knowledge
        res1038 = self.investigate_and_remember(inc1038)
        log_step(6, "Agent Recalls Incident #1024 from Hindsight 🧠", {
            "recalled_incident_id": res1038.recalled_prior_incident.recalled_incident_id if res1038.recalled_prior_incident else "None",
            "similarity_score": res1038.recalled_prior_incident.relevance_score if res1038.recalled_prior_incident else 0.0,
            "match_reason": res1038.recalled_prior_incident.match_reason if res1038.recalled_prior_incident else "",
        })
        log_step(7, "Agent Uses Previous Knowledge", {
            "is_recurring_issue": res1038.is_recurring_issue,
            "recurrence_count": res1038.recurrence_count,
            "recurrence_rationale": res1038.recurrence_rationale,
            "reused_root_cause": res1038.root_cause.summary,
            "reused_remediation": [s.action for s in res1038.remediation_steps],
        })

        # Step 8: Auditor asks for access-control findings
        audit_req = AuditRequest(
            control="Access Control",
            request="Show me previous findings related to access control, their remediation status, and available evidence.",
            requested_by="External SOC2 / ISO Auditor",
        )
        log_step(8, "Auditor Inquires: Access Control Findings", {
            "control": audit_req.control,
            "query": audit_req.request,
        })

        # Step 9 & 10: Agent recalls findings, retrieves evidence + remediation status
        audit_res = self.handle_audit_request(audit_req)
        log_step(9, "Agent Recalls Historical Findings from Hindsight", {
            "historical_findings_count": len(audit_res.historical_findings),
            "findings": [
                {
                    "finding_id": f.finding_id,
                    "incident": f.incident_id,
                    "status": f.status.value,
                    "root_cause": f.root_cause,
                }
                for f in audit_res.historical_findings
            ],
            "recurring_patterns_detected": audit_res.recurring_patterns_detected,
        })
        log_step(10, "Agent Retrieves Evidence + Remediation Status", {
            "evidence_count": len(audit_res.evidence_items),
            "evidence_hashes": [e.hash_digest[:16] + "..." for e in audit_res.evidence_items],
            "compliance_posture": audit_res.compliance_posture,
            "executive_summary": audit_res.executive_summary,
            "auditor_notes": audit_res.auditor_verification_notes,
        })

        return {
            "status": "SUCCESS",
            "message": "Continuous 10-step demo story completed successfully.",
            "steps": logs,
            "inc1024_result": res1024,
            "inc1038_result": res1038,
            "audit_result": audit_res,
        }
