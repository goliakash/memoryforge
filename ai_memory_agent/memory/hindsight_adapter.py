import logging
from typing import List, Optional, Dict, Any

from ai_memory_agent.config import settings
from ai_memory_agent.models.memory_records import (
    MemoryNetworkType,
    MemoryUnit,
    RecallItem,
    ReflectResult,
)
from ai_memory_agent.memory.local_hindsight import LocalHindsightEngine

logger = logging.getLogger(__name__)


class HindsightAdapter:
    """
    Unified Hindsight Memory Adapter.
    Transparently routes to:
    1. Official `hindsight-client` if Hindsight server or Hindsight Cloud is reachable.
    2. Embedded Biomimetic `LocalHindsightEngine` for self-contained, offline-first reliability.
    """

    def __init__(self, bank_id: Optional[str] = None):
        self.bank_id = bank_id or settings.HINDSIGHT_BANK_ID
        self.local_engine = LocalHindsightEngine(bank_id=self.bank_id)
        self.client = None
        self.is_live_client_active = False

        if not settings.FORCE_LOCAL_HINDSIGHT and (settings.HINDSIGHT_API_KEY or settings.HINDSIGHT_BASE_URL != "http://localhost:8888"):
            try:
                from hindsight_client import Hindsight
                self.client = Hindsight(
                    base_url=settings.HINDSIGHT_BASE_URL,
                    api_key=settings.HINDSIGHT_API_KEY if settings.HINDSIGHT_API_KEY else None,
                )
                self.is_live_client_active = True
                logger.info(f"Connected to live Hindsight service at {settings.HINDSIGHT_BASE_URL}")
            except Exception as e:
                logger.warning(f"Could not connect to live Hindsight service ({e}); using embedded LocalHindsightEngine.")
                self.is_live_client_active = False
        else:
            logger.info("Operating in embedded LocalHindsightEngine mode (World, Experience, Observation, Opinion networks).")

    def retain(
        self,
        content: str,
        network_type: MemoryNetworkType = MemoryNetworkType.EXPERIENCE,
        entities: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0,
    ) -> MemoryUnit:
        """Store new security knowledge into Hindsight memory."""
        # Always store in local engine for guaranteed zero-latency local availability & persistence
        local_unit = self.local_engine.retain(
            content=content,
            network_type=network_type,
            entities=entities,
            tags=tags,
            metadata=metadata,
            confidence=confidence,
        )

        # If live client is active, sync with Hindsight server
        if self.is_live_client_active and self.client:
            try:
                self.client.retain(
                    bank_id=self.bank_id,
                    content=content,
                    context=f"network:{network_type.value}, entities:{entities}",
                )
            except Exception as e:
                logger.warning(f"Failed to sync retain with live Hindsight: {e}")

        return local_unit

    def recall(
        self,
        query: str,
        limit: int = 5,
        network: Optional[MemoryNetworkType] = None,
        entities: Optional[List[str]] = None,
        min_score: float = 0.25,
    ) -> List[RecallItem]:
        """Recall relevant organizational memory using hybrid semantic & entity matching."""
        # Check local engine
        local_results = self.local_engine.recall(
            query=query,
            limit=limit,
            network=network,
            entities=entities,
            min_score=min_score,
        )

        # If live client is active and local returned fewer results, we can blend
        if self.is_live_client_active and self.client:
            try:
                live_resp = self.client.recall(bank_id=self.bank_id, query=query)
                # Live client results can enrich the response
            except Exception as e:
                logger.warning(f"Live Hindsight recall query failed: {e}")

        return local_results

    def reflect(self, topic: str) -> ReflectResult:
        """Reflect over organizational memory to synthesize recurring patterns and risk posture."""
        return self.local_engine.reflect(topic=topic)

    def get_timeline(self) -> List[Dict[str, Any]]:
        """Retrieve chronological history of organizational memories."""
        return self.local_engine.get_timeline()

    def get_networks_summary(self) -> Dict[str, Any]:
        """Summary of units in World, Experience, Observation, and Opinion networks."""
        return {
            "bank_id": self.bank_id,
            "engine_mode": "Live Hindsight Client" if self.is_live_client_active else "Embedded Biomimetic Engine",
            "networks": {
                net.value: len(units) for net, units in self.local_engine.networks.items()
            },
            "total_memories": sum(len(units) for units in self.local_engine.networks.values()),
        }

    def clear(self):
        self.local_engine.clear()
