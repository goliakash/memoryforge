import pytest
from ai_memory_agent.memory.local_hindsight import LocalHindsightEngine
from ai_memory_agent.memory.hindsight_adapter import HindsightAdapter
from ai_memory_agent.models.memory_records import MemoryNetworkType


def test_hindsight_baseline_world_network():
    engine = LocalHindsightEngine()
    world_units = engine.networks[MemoryNetworkType.WORLD]
    assert len(world_units) >= 3
    assert any("SOC2-CC6.1" in u.content for u in world_units)


def test_hindsight_retain_and_recall():
    engine = LocalHindsightEngine()
    engine.clear()

    # Retain test experience
    unit = engine.retain(
        content="Incident INC-999: S3 storage bucket exposed with public read ACL. Remediation: blocked public access.",
        network_type=MemoryNetworkType.EXPERIENCE,
        entities=["INC-999", "S3", "Access Control"],
        tags=["s3", "incident"],
        metadata={"incident_id": "INC-999", "root_cause": "Permissive ACL"},
    )
    assert unit.id.startswith("experience-")

    # Recall
    results = engine.recall(query="public read ACL storage bucket", limit=3)
    assert len(results) >= 1
    top_result = results[0]
    assert top_result.score > 0.4
    assert "INC-999" in top_result.memory_unit.content


def test_hindsight_proactive_synthesis_and_reflect():
    engine = LocalHindsightEngine()
    engine.clear()

    # Retain two similar experiences
    engine.retain(
        content="Incident INC-01: Cloud storage bucket exposed due to incorrect access policy.",
        network_type=MemoryNetworkType.EXPERIENCE,
        entities=["INC-01", "Access Control"],
        metadata={"incident_id": "INC-01", "root_cause": "incorrect access policy", "asset_type": "cloud_storage", "controls": ["SOC2-CC6.1"]},
    )

    engine.retain(
        content="Incident INC-02: Cloud storage bucket exposed due to incorrect access policy.",
        network_type=MemoryNetworkType.EXPERIENCE,
        entities=["INC-02", "Access Control"],
        metadata={"incident_id": "INC-02", "root_cause": "incorrect access policy", "asset_type": "cloud_storage", "controls": ["SOC2-CC6.1"]},
    )

    # Check proactive synthesis created Observation and Opinion
    obs_units = engine.networks[MemoryNetworkType.OBSERVATION]
    op_units = engine.networks[MemoryNetworkType.OPINION]
    assert len(obs_units) >= 1
    assert len(op_units) >= 1

    # Reflect
    reflection = engine.reflect(topic="Access Control")
    assert reflection.topic == "Access Control"
    assert len(reflection.recurring_patterns) >= 1
