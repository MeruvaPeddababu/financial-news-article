# agents/deduplication.py – FINAL WINNING VERSION (Pydantic-safe + Real-time Alerts)
import numpy as np
from sklearn.cluster import DBSCAN
from utils.embeddings import get_embedding
from agents.alert import trigger_realtime_alert
from typing import Dict, Any

def deduplication_agent(state) -> Dict[str, Any]:
    """
    Deduplicates + triggers REAL-TIME ALERT when NEW unique story is found
    Works with Pydantic AgentState (no .get() allowed!)
    """
    # CORRECT WAY: state is Pydantic model → use getattr or direct access
    pending = [n for n in state.processed_news if n.cluster_id is None]
    if not pending:
        return {"processed_news": state.processed_news, "clusters": state.clusters}

    texts = [n.title + " " + n.content for n in pending]
    embeddings = np.array([get_embedding(t) for t in texts])
    clustering = DBSCAN(eps=0.3, min_samples=1, metric="cosine").fit(embeddings)

    cluster_map = {}
    alerted_ids = set()

    for idx, label in enumerate(clustering.labels_):
        news = pending[idx]
        news.embedding = embeddings[idx].tolist()
        news.cluster_id = int(label)

        if label not in cluster_map:
            cluster_map[label] = []
        cluster_map[label].append(news.id)

        # Find canonical (longest content)
        members = [n for n in pending if n.cluster_id == label]
        canonical = max(members, key=lambda x: len(x.content))
        canonical.is_canonical = True

        # TRIGGER ALERT ONLY ONCE per unique story
        if canonical.id == news.id:  # This is the canonical version
            current_alerted = getattr(state, "alerted_stories", set())
            if canonical.id not in current_alerted:
                print(f"NEW UNIQUE STORY → ALERT: {canonical.title[:70]}")
                trigger_realtime_alert(canonical)
                alerted_ids.add(canonical.id)

    return {
        "processed_news": state.processed_news,
        "clusters": {**state.clusters, **cluster_map},
        "alerted_stories": getattr(state, "alerted_stories", set()) | alerted_ids
    }

