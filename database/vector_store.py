# database/vector_store.py – FINAL 100% WORKING VERSION
import chromadb
from utils.embeddings import get_embedding
from models import ProcessedNews
from typing import List

# ChromaDB setup
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="financial_news")

def add_news(news: ProcessedNews):
    """
    Add a single ProcessedNews object to ChromaDB
    Required by storage_agent
    """
    if news.embedding is None:
        news.embedding = get_embedding(news.title + " " + news.content)

    collection.add(
        ids=[news.id],
        embeddings=[news.embedding],
        documents=[news.title + "\n\n" + news.content],
        metadatas={
            "news_id": news.id,
            "cluster_id": news.cluster_id or -1,
            "is_canonical": news.is_canonical,
            "source": news.source,
            "published_at": news.published_at.isoformat(),
            "title": news.title
        }
    )

def search(query: str, top_k: int = 15) -> dict:
    """
    Semantic search used by query_agent
    """
    query_emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k * 3,
        include=["metadatas", "documents", "distances"]
    )
    
    # Safely extract IDs
    ids = []
    for meta in results["metadatas"][0]:
        if meta and isinstance(meta, dict):
            ids.append(meta.get("news_id") or meta.get("id"))
    
    return {
        "ids": [ids],
        "metadatas": [{"id": i} for i in ids if i],
        "documents": results["documents"][0]
    }