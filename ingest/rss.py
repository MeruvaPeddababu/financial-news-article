# ingest/rss.py – FINAL LIGHTNING-FAST + ASYNC VERSION
import aiohttp
import feedparser
import asyncio
from typing import List, Dict
from datetime import datetime
import uuid

async def fetch_single_rss(session, url: str) -> List[Dict]:
    """Fetch one RSS feed asynchronously"""
    try:
        async with session.get(url, timeout=15) as response:
            if response.status != 200:
                return []
            text = await response.text()
            
        feed = feedparser.parse(text)
        articles = []
        
        for entry in feed.entries[:30]:
            articles.append({
                "id": str(uuid.uuid4()),
                "title": entry.get("title", "No title"),
                "content": entry.get("summary", "") or entry.get("description", "") or "",
                "url": entry.get("link", ""),
                "source": feed.feed.get("title", url),
                "published_at": entry.get("published") or datetime.now().isoformat()
            })
        return articles
    except Exception as e:
        print(f"RSS failed: {url} → {e}")
        return []

async def ingest_multiple_rss(urls: List[str]) -> List[Dict]:
    """Fetch ALL RSS feeds in parallel — 10x faster!"""
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_single_rss(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_articles = []
    for result in results:
        if isinstance(result, list):
            all_articles.extend(result)
    
    return all_articles