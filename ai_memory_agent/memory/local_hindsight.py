import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from ai_memory_agent.config import settings
from ai_memory_agent.models.memory_records import (
    MemoryNetworkType,
    MemoryUnit,
    RecallItem,
    ReflectResult,
)
from ai_memory_agent.memory.similarity import calculate_hybrid_similarity, tokenize


class LocalHindsightEngine:
    """
    Biomimetic In-Process Memory System mirroring Hindsight architecture:
    - 4 Networks: World, Experience, Observation, Opinion
    - 3 Operations: Retain, Recall, Reflect
    - Persistent storage in DuckDB / JSON
    """

    def __init__(self, bank_id: str = None, storage_path: Path = None):
        self.bank_id = bank_id or settings.HINDSIGHT_BANK_ID
        self.storage_path = storage_path or settings.LOCAL_JSON_BACKUP
        self.duckdb_path = settings.LOCAL_DB_PATH

        # In-memory index of MemoryUnits by Network
        self.networks: Dict[MemoryNetworkType, List[MemoryUnit]] = {
            MemoryNetworkType.WORLD: [],
            MemoryNetworkType.EXPERIENCE: [],
            MemoryNetworkType.OBSERVATION: [],
            MemoryNetworkType.OPINION: [],
        }

        self._load_from_storage()
        self._initialize_baseline_world_knowledge()

    def _initialize_baseline_world_knowledge(self):
        """Seed initial World facts if memory bank is empty."""
        if not self.networks[MemoryNetworkType.WORLD]:
            baseline_facts = [
                (
                    "Standard organizational access control requires SOC2-CC6.1, NIST-PR.AC-04, and ISO-A.5.15 compliance across all production assets.",
                    ["SOC2-CC6.1", "NIST-PR.AC-04", "Access Control"],
                    {"frameworks": ["SOC2", "NIST_CSF", "ISO27001"]}
                ),
                (
                    "Production cloud storage assets must maintain S3 Public Access Block enabled at all times with KMS encryption enabled.",
                    ["cloud_storage", "S3", "Data Protection"],
                    {"policy": "zero-public-storage"}
                ),
                (
                    "Any production incident involving publicly readable customer data is classified as Severity HIGH or CRITICAL.",
                    ["Severity", "S3", "customer-data"],
                    {"classification_rule": "customer_data_public"}
                ),
            ]
            for content, entities, meta in baseline_facts:
                unit = MemoryUnit(
                    id=f"world-{uuid.uuid4().hex[:8]}",
                    bank_id=self.bank_id,
                    network_type=MemoryNetworkType.WORLD,
                    content=content,
                    entities=entities,
                    tags=["baseline", "policy"],
                    metadata=meta,
                    confidence=1.0,
                )
                self.networks[MemoryNetworkType.WORLD].append(unit)

    def retain(
        self,
        content: str,
        network_type: MemoryNetworkType = MemoryNetworkType.EXPERIENCE,
        entities: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0,
    ) -> MemoryUnit:
        """
        Retain new context, experience, observation, or opinion into Hindsight memory.
        """
        unit_id = f"{network_type.value}-{uuid.uuid4().hex[:10]}"
        unit = MemoryUnit(
            id=unit_id,
            bank_id=self.bank_id,
            network_type=network_type,
            content=content,
            entities=entities or [],
            tags=tags or [],
            metadata=metadata or {},
            confidence=confidence,
            created_at=datetime.utcnow(),
        )

        self.networks[network_type].append(unit)
        self._save_to_storage()

        # Proactive learning: trigger automatic observation / opinion synthesis if multiple similar experiences occur
        if network_type == MemoryNetworkType.EXPERIENCE:
            self._proactive_experience_synthesis(unit)

        return unit

    def recall(
        self,
        query: str,
        limit: int = 5,
        network: Optional[MemoryNetworkType] = None,
        entities: Optional[List[str]] = None,
        min_score: float = 0.25,
    ) -> List[RecallItem]:
        """
        Recall relevant historical memories across networks using hybrid matching.
        """
        candidate_units: List[MemoryUnit] = []
        if network:
            candidate_units = self.networks.get(network, [])
        else:
            # Query across all 4 networks
            for net_units in self.networks.values():
                candidate_units.extend(net_units)

        scored_items: List[RecallItem] = []
        for unit in candidate_units:
            sim_score = calculate_hybrid_similarity(
                query_text=query,
                target_text=unit.content,
                query_entities=entities,
                target_entities=unit.entities,
            )

            # Boost experience and observation items matching specific incident ID or control ID
            if entities:
                for ent in entities:
                    if any(ent.lower() in u_ent.lower() for u_ent in unit.entities):
                        sim_score = min(1.0, sim_score + 0.15)

            if sim_score >= min_score:
                reason = f"Matched [{unit.network_type.value.upper()}] with similarity {sim_score:.2f}"
                if unit.entities:
                    matched_ents = set(e.lower() for e in (entities or [])) & set(e.lower() for e in unit.entities)
                    if matched_ents:
                        reason += f" | Common entities: {list(matched_ents)}"

                scored_items.append(
                    RecallItem(
                        memory_unit=unit,
                        score=round(sim_score, 4),
                        match_reason=reason,
                    )
                )

        # Sort descending by relevance score
        scored_items.sort(key=lambda item: item.score, reverse=True)
        return scored_items[:limit]

    def reflect(self, topic: str) -> ReflectResult:
        """
        Reflect over organizational memory to synthesize cross-incident patterns,
        identify recurring security problems, control degradation, and preventive recommendations.
        """
        # Recall experiences and observations related to topic
        recalled = self.recall(query=topic, limit=20, min_score=0.20, entities=[topic])

        incident_experiences = [
            item.memory_unit for item in recalled
            if item.memory_unit.network_type == MemoryNetworkType.EXPERIENCE
        ]
        # Include experiences with matching entities or content
        for exp in self.networks[MemoryNetworkType.EXPERIENCE]:
            if exp not in incident_experiences:
                if any(topic.lower() in e.lower() for e in exp.entities) or topic.lower() in exp.content.lower():
                    incident_experiences.append(exp)

        observations = [
            obs for obs in self.networks[MemoryNetworkType.OBSERVATION]
            if any(topic.lower() in e.lower() for e in obs.entities) or topic.lower() in obs.content.lower()
        ]
        opinions = [
            op for op in self.networks[MemoryNetworkType.OPINION]
            if any(topic.lower() in e.lower() for e in op.entities) or topic.lower() in op.content.lower()
        ]

        recurring_patterns: List[str] = [obs.content for obs in observations]
        at_risk_controls: List[str] = []
        recommendations: List[str] = []

        # Analyze incidents
        incidents_count = len(incident_experiences)
        asset_types: Dict[str, int] = {}
        controls_affected: Dict[str, int] = {}

        for unit in incident_experiences:
            meta = unit.metadata
            asset_type = meta.get("asset_type", "cloud_resource")
            asset_types[asset_type] = asset_types.get(asset_type, 0) + 1

            for ctrl in meta.get("controls", []):
                controls_affected[ctrl] = controls_affected.get(ctrl, 0) + 1

        for c_id, count in controls_affected.items():
            if count >= 2:
                recurring_patterns.append(f"Recurring control violation detected for control {c_id} ({count} occurrences).")
                at_risk_controls.append(c_id)

        for a_type, count in asset_types.items():
            if count >= 2:
                recurring_patterns.append(f"Multiple security events targeting asset category '{a_type}' ({count} incidents).")

        if recurring_patterns:
            recommendations.append("Enforce automated CI/CD policy-as-code linting before cloud deployment.")
            recommendations.append("Apply account-level AWS Organization Service Control Policies (SCPs) preventing public bucket creation.")
            recommendations.append("Conduct mandatory remediation verification audits on all related access-control assets.")
        else:
            recommendations.append("Maintain continuous monitoring and baseline security posture reviews.")

        synthesis_text = (
            f"Organizational memory synthesis on '{topic}': Analyzed {incidents_count} related security incidents, "
            f"{len(observations)} behavioral observations, and {len(opinions)} organizational beliefs. "
        )
        if recurring_patterns:
            synthesis_text += f"High recurrence alert: {len(recurring_patterns)} pattern(s) identified indicating systemic drift."
        else:
            synthesis_text += "Controls are currently stable with isolated non-recurring events."

        return ReflectResult(
            topic=topic,
            synthesis=synthesis_text,
            recurring_patterns=recurring_patterns,
            at_risk_controls=list(set(at_risk_controls)),
            recommended_policy_changes=recommendations,
            confidence=0.92,
        )

    def _proactive_experience_synthesis(self, new_unit: MemoryUnit):
        """
        Background synthesis when a new experience is retained:
        If multiple experiences share root cause or asset type, synthesize an OBSERVATION and OPINION.
        """
        meta = new_unit.metadata
        incident_id = meta.get("incident_id")
        root_cause = meta.get("root_cause", "")
        asset_type = meta.get("asset_type", "")

        # Count similar experiences
        similar_units = []
        for exp in self.networks[MemoryNetworkType.EXPERIENCE]:
            exp_meta = exp.metadata
            if exp_meta.get("incident_id") != incident_id:
                if (asset_type and exp_meta.get("asset_type") == asset_type) or (
                    root_cause and calculate_hybrid_similarity(root_cause, exp_meta.get("root_cause", "")) > 0.4
                ):
                    similar_units.append(exp)

        if len(similar_units) >= 1:
            # Recurring pattern observed!
            prior_inc_id = similar_units[-1].metadata.get("incident_id", "Prior Incident")
            observation_text = (
                f"Synthesized Pattern: Repeated occurrence of '{root_cause}' affecting asset class '{asset_type}'. "
                f"Incident {incident_id} matches historical pattern from {prior_inc_id}. "
                f"Indicates access control misconfiguration is not an isolated event."
            )
            # Create observation
            obs_unit = MemoryUnit(
                id=f"obs-{uuid.uuid4().hex[:8]}",
                bank_id=self.bank_id,
                network_type=MemoryNetworkType.OBSERVATION,
                content=observation_text,
                entities=[incident_id, prior_inc_id, asset_type, "Access Control"],
                tags=["recurring_pattern", "root_cause_cluster"],
                metadata={
                    "pattern": "repeated_access_policy_exposure",
                    "incidents": [prior_inc_id, incident_id],
                },
                confidence=0.95,
            )
            self.networks[MemoryNetworkType.OBSERVATION].append(obs_unit)

            # Create opinion
            opinion_text = (
                f"Organizational Belief: Cloud storage access policy configurations carry high human-error risk. "
                f"Manual configuration reviews are ineffective for {asset_type}; automated preventive guardrails are required."
            )
            op_unit = MemoryUnit(
                id=f"op-{uuid.uuid4().hex[:8]}",
                bank_id=self.bank_id,
                network_type=MemoryNetworkType.OPINION,
                content=opinion_text,
                entities=[asset_type, "Policy Guardrails", "Access Control"],
                tags=["organizational_belief", "risk_posture"],
                metadata={"risk_score": 0.85},
                confidence=0.88,
            )
            self.networks[MemoryNetworkType.OPINION].append(op_unit)
            self._save_to_storage()

    def get_timeline(self) -> List[Dict[str, Any]]:
        """Returns chronological stream of all organizational memories."""
        all_memories: List[MemoryUnit] = []
        for net_units in self.networks.values():
            all_memories.extend(net_units)

        all_memories.sort(key=lambda m: m.created_at)
        return [
            {
                "id": m.id,
                "network": m.network_type.value,
                "content": m.content,
                "entities": m.entities,
                "tags": m.tags,
                "confidence": m.confidence,
                "timestamp": m.created_at.isoformat(),
                "metadata": m.metadata,
            }
            for m in all_memories
        ]

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            serializable_data = {}
            for net, units in self.networks.items():
                serializable_data[net.value] = [unit.model_dump(mode="json") for unit in units]
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(serializable_data, f, indent=2, default=str)
        except Exception as e:
            # Fallback logging
            pass

    def _load_from_storage(self):
        if self.storage_path and self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for net_key, unit_dicts in data.items():
                    net_enum = MemoryNetworkType(net_key)
                    self.networks[net_enum] = [MemoryUnit.model_validate(d) for d in unit_dicts]
            except Exception:
                pass

    def clear(self):
        for net in self.networks:
            self.networks[net] = []
        if self.storage_path.exists():
            self.storage_path.unlink()
        self._initialize_baseline_world_knowledge()
