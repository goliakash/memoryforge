import time
from typing import Optional, List, Dict, Any
from datetime import datetime

from ai_memory_agent.agents.base_agent import BaseAgent
from ai_memory_agent.models.incident import Incident
from ai_memory_agent.models.investigation import (
    RootCause,
    MITRETechnique,
    PostMortem,
    RecalledMemoryContext,
)
from ai_memory_agent.models.memory_records import MemoryNetworkType, RecallItem


class SecurityInvestigationAgent(BaseAgent):
    """
    Member 1 Focus: Security Investigation Agent.
    - Incident Ingestion & Triage
    - Hindsight Memory Recall for Prior Incidents
    - Root-Cause Analysis (RCA)
    - MITRE ATT&CK Mapping
    - Recurrence Detection
    - Post-Mortem Generation
    """

    def recall_prior_incidents(self, incident: Incident) -> Optional[RecalledMemoryContext]:
        """
        Query Hindsight Experience Network to find if a similar incident
        was previously investigated and resolved.
        """
        query_text = f"{incident.title} {incident.description} {incident.affected_asset} {incident.evidence}"
        entities = [incident.incident_id, incident.affected_asset, incident.asset_type]

        # Recall from Experience network
        recalled_items: List[RecallItem] = self.memory.recall(
            query=query_text,
            limit=3,
            network=MemoryNetworkType.EXPERIENCE,
            entities=entities,
            min_score=0.30,
        )

        for item in recalled_items:
            unit = item.memory_unit
            meta = unit.metadata
            prior_inc_id = meta.get("incident_id")

            # Must be a distinct previous incident
            if prior_inc_id and prior_inc_id != incident.incident_id:
                return RecalledMemoryContext(
                    recalled_incident_id=prior_inc_id,
                    recalled_title=meta.get("title", "Prior Security Incident"),
                    relevance_score=item.score,
                    recalled_root_cause=meta.get("root_cause", "Misconfiguration identified"),
                    recalled_remediations=meta.get("remediations", []),
                    recalled_controls=meta.get("controls", []),
                    match_reason=item.match_reason,
                )

        return None

    def investigate(
        self,
        incident: Incident,
        recalled_context: Optional[RecalledMemoryContext] = None,
    ) -> Dict[str, Any]:
        """
        Executes AI Investigation over the incident, augmented by recalled Hindsight memory.
        """
        start_time = time.time()

        history_str = ""
        if recalled_context:
            history_str = (
                f"RECALLED PRIOR INCIDENT: {recalled_context.recalled_incident_id} ({recalled_context.recalled_title})\n"
                f"Similarity Score: {recalled_context.relevance_score:.2f}\n"
                f"Previous Root Cause: {recalled_context.recalled_root_cause}\n"
                f"Previous Proven Remediation: {', '.join(recalled_context.recalled_remediations)}\n"
                f"Previous Controls: {', '.join(recalled_context.recalled_controls)}"
            )

        incident_dict = {
            "incident_id": incident.incident_id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity.value,
            "affected_asset": incident.affected_asset,
            "asset_type": incident.asset_type,
            "evidence": incident.evidence,
        }

        analysis = self.llm.analyze_incident(
            incident_data=incident_dict,
            historical_context=history_str,
        )

        # Parse Root Cause
        rc_data = analysis["root_cause"]
        root_cause = RootCause(
            category=rc_data["category"],
            summary=rc_data["summary"],
            technical_details=rc_data["technical_details"],
            confidence=rc_data.get("confidence", 0.95),
            contributing_factors=rc_data.get("contributing_factors", []),
        )

        # Parse MITRE Techniques
        mitre_techniques = [
            MITRETechnique(
                technique_id=m["technique_id"],
                name=m["name"],
                tactic=m["tactic"],
            )
            for m in analysis.get("mitre_techniques", [])
        ]

        # Parse Post-Mortem
        pm_data = analysis["post_mortem"]
        timeline = [
            f"{incident.detected_at.strftime('%Y-%m-%d %H:%M:%S')} UTC - Detection alert triggered: {incident.evidence[:60]}...",
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC - AI Investigation initiated using Hindsight memory recall.",
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC - Root cause identified as '{root_cause.category}'.",
        ]
        if recalled_context:
            timeline.insert(
                1,
                f"Hindsight Recall: Correlated with historical Incident {recalled_context.recalled_incident_id} (Score: {recalled_context.relevance_score:.2f})."
            )

        post_mortem = PostMortem(
            post_mortem_id=f"PM-{incident.incident_id}",
            incident_id=incident.incident_id,
            incident_title=incident.title,
            executive_summary=pm_data.get("executive_summary", f"Post-mortem for {incident.incident_id}"),
            timeline=timeline,
            root_cause=pm_data.get("root_cause", root_cause.summary),
            impact_blast_radius=pm_data.get("impact_blast_radius") or pm_data.get("blast_radius", f"Restricted to {incident.affected_asset}"),
            lessons_learned=pm_data.get("lessons_learned", []),
            preventive_actions=pm_data.get("preventive_actions", []),
            created_at=datetime.utcnow(),
        )

        # Determine recurrence
        is_recurring = bool(recalled_context is not None and recalled_context.relevance_score >= 0.35)
        recurrence_rationale = None
        if is_recurring:
            recurrence_rationale = (
                f"Incident {incident.incident_id} matches historical Incident {recalled_context.recalled_incident_id}. "
                f"Both stem from {root_cause.category} on cloud storage assets. "
                f"Prior investigation knowledge reused to accelerate resolution."
            )

        elapsed_ms = (time.time() - start_time) * 1000

        return {
            "root_cause": root_cause,
            "mitre_techniques": mitre_techniques,
            "post_mortem": post_mortem,
            "recalled_prior_incident": recalled_context,
            "is_recurring_issue": is_recurring,
            "recurrence_count": 2 if is_recurring else 1,
            "recurrence_rationale": recurrence_rationale,
            "execution_time_ms": round(elapsed_ms, 2),
        }
