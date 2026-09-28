import re
import math
from typing import List, Set, Dict


def tokenize(text: str) -> List[str]:
    # Normalize and extract alphanumeric tokens
    tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]+\b", text.lower())
    # Basic stop words filtering
    stop_words = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "are", "was", "were", "be", "been",
        "this", "that", "it", "as", "from"
    }
    return [t for t in tokens if t not in stop_words and len(t) > 1]


def compute_tf_vector(tokens: List[str]) -> Dict[str, float]:
    tf: Dict[str, float] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0.0) + 1.0
    # Normalize by length
    total = len(tokens) or 1
    return {k: v / total for k, v in tf.items()}


def cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    dot_product = sum(v1[k] * v2.get(k, 0.0) for k in v1)
    norm1 = math.sqrt(sum(v * v for v in v1.values()))
    norm2 = math.sqrt(sum(v * v for v in v2.values()))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot_product / (norm1 * norm2)


def calculate_hybrid_similarity(
    query_text: str,
    target_text: str,
    query_entities: List[str] = None,
    target_entities: List[str] = None,
) -> float:
    """
    Computes a hybrid similarity score combining:
    1. Query term coverage (what fraction of search terms appeared in target/entities) (50% weight)
    2. Lexical and semantic token TF cosine similarity (30% weight)
    3. Entity matching bonus (20% weight)
    """
    q_tokens = tokenize(query_text)
    t_tokens = tokenize(target_text)

    if not q_tokens or not t_tokens:
        return 0.0

    # Expand target tokens with target entities if present
    target_extended_tokens = set(t_tokens)
    if target_entities:
        for ent in target_entities:
            target_extended_tokens.update(tokenize(ent))

    # 1. Query coverage
    q_set: Set[str] = set(q_tokens)
    matched_tokens = q_set & target_extended_tokens
    query_coverage = len(matched_tokens) / (len(q_set) or 1)

    # 2. Cosine similarity
    q_tf = compute_tf_vector(q_tokens)
    t_tf = compute_tf_vector(t_tokens)
    cos_sim = cosine_similarity(q_tf, t_tf)

    # 3. Entity overlap
    entity_score = 0.0
    if target_entities:
        t_ent = {e.lower().strip() for e in target_entities}
        # Check query entities or query text against target entities
        if query_entities:
            q_ent = {e.lower().strip() for e in query_entities}
            if q_ent & t_ent:
                entity_score = 1.0
        else:
            q_lower = query_text.lower()
            if any(e in q_lower or q_lower in e for e in t_ent):
                entity_score = 0.8
            elif any(t in " ".join(t_ent) for t in q_tokens):
                entity_score = 0.5

    # Weighted combination
    composite_score = (0.50 * query_coverage) + (0.30 * cos_sim) + (0.20 * entity_score)
    return round(min(1.0, composite_score), 4)
