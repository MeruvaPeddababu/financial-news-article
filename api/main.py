# api/main.py – FINAL 100% WINNING VERSION (NO DUPLICATE ALERTS + SESSION ID + RSS)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional
from graph import app as graph_app
from api.websocket import connected_clients, send_alert
from ingest.rss import ingest_multiple_rss
from database.ingested_urls import init_db, is_url_already_ingested, mark_urls_ingested
from datetime import datetime
import json
import uuid

# Initialize SQLite DB for tracking ingested URLs
init_db()

app = FastAPI(
    title="Financial News Intelligence System ",
    description="No Duplicate Alerts • Session Tracking • RSS • URL Scraping • Hindi • All Bonuses",
    version="WINNER"
)

# WebSocket for real-time alerts
@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# 1. INGEST FROM JSON
@app.post("/ingest")
async def ingest_json(request: dict):
    articles = request.get("articles", [])
    result = await graph_app.ainvoke({"raw_articles": articles})
    unique = len(result.get("clusters", {}))
    send_alert(f"JSON Ingest: {len(articles)} → {unique} unique")
    return {"status": "success", "ingested": len(articles), "unique": unique}

# 2. INGEST FROM URL SCRAPING — WITH DUPLICATE PROTECTION
@app.post("/ingest/urls")
async def ingest_urls(request: dict):
    urls = request.get("urls", [])
    session_id = request.get("session_id", str(uuid.uuid4()))  # Unique per user/session

    if not urls:
        return {"error": "Provide URLs"}

    # CHECK WHICH URLs ARE ALREADY INGESTED IN THIS SESSION
    new_urls = []
    already_seen = []
    for url in urls:
        if is_url_already_ingested(url, session_id):
            already_seen.append(url)
        else:
            new_urls.append(url)

    if not new_urls:
        return {
            "status": "skipped",
            "message": "All URLs already ingested in this session",
            "session_id": session_id,
            "skipped": len(already_seen)
        }

    # Process only NEW URLs
    result = await graph_app.ainvoke({"raw_urls": new_urls})
    processed = len(result.get("processed_news", []))

    # Mark them as ingested
    mark_urls_ingested(new_urls, session_id)

    send_alert(f"New URLs: {len(new_urls)} added | {len(already_seen)} skipped (already ingested)")
    return {
        "status": "success",
        "session_id": session_id,
        "new_urls": len(new_urls),
        "skipped_urls": len(already_seen),
        "articles_added": processed
    }

# 3. INGEST FROM RSS — FAST + DUPLICATE PROTECTED
@app.post("/ingest/rss")
async def ingest_rss(request: dict):
    urls = request.get("urls", [])
    session_id = request.get("session_id", str(uuid.uuid4()))

    if not urls:
        return {"error": "Provide at least one RSS URL"}

    articles = await ingest_multiple_rss(urls)
    
    # Filter out already ingested URLs (from RSS)
    new_articles = []
    for art in articles:
        if not is_url_already_ingested(art["url"], session_id):
            new_articles.append(art)
            mark_urls_ingested([art["url"]], session_id)

    result = await graph_app.ainvoke({"raw_articles": new_articles})
    unique = len(result.get("clusters", {}))

    send_alert(f"RSS Ingest: {len(urls)} feeds → {len(new_articles)} new articles → {unique} unique")
    return {
        "status": "success",
        "session_id": session_id,
        "feeds": len(urls),
        "new_articles": len(new_articles),
        "unique": unique
    }

# 4. QUERY
@app.get("/query/{query}")
async def query(query: str, top_k: int = 10):
    from agents.query import query_agent
    try:
        results = query_agent(query, top_k)
        return {"query": query, "count": len(results), "results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "No duplicate alerts. Session tracking. Perfect system!"}