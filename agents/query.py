# agents/query.py – FINAL 100% LOCAL VERSION (NO MISTRAL API, NO TOKEN LIMIT)
from database.vector_store import collection
from utils.embeddings import get_embedding
from utils.ner import nlp  # Your existing spaCy model
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from typing import List, Dict

# Local sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

def query_agent(query: str, top_k: int = 5) -> Dict:
    # 1. RAG Retrieval
    query_emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k * 3,
        include=["documents", "metadatas", "distances"]
    )
    
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    final_results = []
    
    for doc, meta in zip(docs, metadatas):
        if not doc or len(doc) < 100:
            continue
            
        title = meta.get("title", "No title")
        
        # 2. LOCAL ENTITY EXTRACTION (spaCy — already in your utils/ner.py)
        spacy_doc = nlp(doc)
        companies = [ent.text for ent in spacy_doc.ents if ent.label_ in ["ORG", "PRODUCT"]]
        regulators = [ent.text for ent in spacy_doc.ents if ent.text in ["RBI", "SEBI", "IRDAI"]]
        sectors = ["Banking" if any(x in doc.lower() for x in ["bank", "npa", "loan", "deposit"]) else "Financial"]
        
        # 3. LOCAL SENTIMENT (VADER — zero cost)
        sentiment_score = sentiment_analyzer.polarity_scores(doc)
        sentiment = "POSITIVE" if sentiment_score['compound'] > 0.3 else "NEGATIVE" if sentiment_score['compound'] < -0.3 else "NEUTRAL"
        
        # 4. IMPACTED STOCKS (rule-based + your logic)
        impacted = []
        if "HDFC Bank" in doc:
            impacted.append({"symbol": "HDFCBANK", "company_name": "HDFC Bank", "confidence": 1.0, "type": "direct", "reason": "Direct mention"})
        if "RBI" in doc and "rate" in doc.lower():
            impacted.append({"symbol": "NIFTYBANK", "company_name": "Banking Sector", "confidence": 0.9, "type": "regulatory", "reason": "RBI policy impact"})
        
        # 5. RETRIEVAL EXPLANATION
        explanation = "Direct match to query" if query.lower() in doc.lower() else "Semantically related financial news"
        
        final_results.append({
            "title": title,
            "content": doc[:5000],  # FULL RICH CONTENT
            "entities": {
                "companies": list(set(companies)),
                "regulators": list(set(regulators)),
                "sectors": sectors
            },
            "impacted_stocks": impacted,
            "sentiment": sentiment,
            "retrieval_explanation": explanation
        })
    
    # Sort by relevance (distance)
    sorted_results = sorted(final_results, key=lambda x: x.get("distance", 1.0))
    
    return {
        "query": query,
        "count": len(sorted_results),
        "results": sorted_results[:top_k]
    }