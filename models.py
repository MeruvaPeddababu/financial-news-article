# models.py – FINAL 100% CLEAN & WINNING (Pydantic v2 Compatible)
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ImpactType(str, Enum):
    DIRECT = "direct"
    SECTOR = "sector"
    REGULATORY = "regulatory"
    THEMATIC = "thematic"

class StockImpact(BaseModel):
    symbol: str
    company_name: str
    confidence: float
    type: ImpactType
    reason: str

class NewsEntity(BaseModel):
    text: str
    label: str
    symbol: Optional[str] = None

class ProcessedNews(BaseModel):
    id: str
    title: str
    content: str
    url: Optional[str] = None
    published_at: datetime
    source: str
    entities: List[NewsEntity] = []
    impacts: List[StockImpact] = []
    embedding: Optional[List[float]] = None
    cluster_id: Optional[int] = None
    is_canonical: bool = False

# FINAL AGENT STATE — 100% Pydantic v2 + LangGraph Compatible
class AgentState(BaseModel):
    raw_urls: List[str] = []
    raw_articles: List[Dict[str, Any]] = []
    processed_news: List[ProcessedNews] = []
    clusters: Dict[int, List[str]] = {}
    alerted_stories: Set[str] = set()    # ← Prevents duplicate alerts
    messages: List[str] = []

    model_config = {
        "arbitrary_types_allowed": True,
        # allow_mutation is REMOVED — it's default True in Pydantic v2
        # LangGraph works perfectly without it
    }