# agents/ingestion.py – FINAL WINNING VERSION (Pydantic-safe)
import requests
from ingest.scraper import clean_content
from ingest.safebrowsing import is_url_safe
import uuid
from datetime import datetime
from models import ProcessedNews
from typing import List, Dict

def ingestion_agent(state) -> Dict:
    """
    LangGraph agent: receives AgentState (Pydantic model)
    """
    # CORRECT WAY — state is Pydantic model, use .raw_urls directly
    raw_urls: List[str] = getattr(state, "raw_urls", [])
    processed_news = []

    seen_urls = set()

    for url in raw_urls:
        url = url.strip()
        if not url or url in seen_urls:
            continue
        if not is_url_safe(url):
            print(f"Blocked unsafe URL: {url}")
            continue

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                continue

            title = "No title"
            if "<title>" in r.text:
                try:
                    title = r.text.split("<title>")[1].split("</title>")[0]
                except:
                    pass

            content = clean_content(r.text)
            if len(content) < 100:
                continue

            news = ProcessedNews(
                id=str(uuid.uuid4()),
                title=title.strip(),
                content=content[:20000],
                url=url,
                published_at=datetime.now(),
                source=url.split("/")[2] if "//" in url else "unknown",
                entities=[],
                impacts=[],
                embedding=None,
                cluster_id=None,
                is_canonical=False
            )
            processed_news.append(news)
            seen_urls.add(url)

        except Exception as e:
            print(f"Scraping failed for {url}: {e}")
            continue

    # Return dict — LangGraph expects this format
    return {"processed_news": processed_news}