# ingest/scraper.py – FINAL 100% WINNING VERSION (MAXIMUM CONTENT + PROFESSIONAL CLEANING)
import requests
from bs4 import BeautifulSoup
import re
from typing import Optional

def clean_content(html: str, url: Optional[str] = None) -> str:
    """
    Extracts the richest, longest, cleanest article content possible
    Returns up to 50,000 characters — perfect for Mistral AI
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. REMOVE ALL JUNK
    for selector in [
        "script", "style", "nav", "header", "footer", "sidebar", 
        "advertisement", "ad-", "banner", "cookie", "popup", "modal",
        "social-share", "related-articles", "comments", "disqus", "share-bar"
    ]:
        for tag in soup.find_all(class_=re.compile(selector, re.I)) or []:
            tag.decompose()
        for tag in soup.find_all(id=re.compile(selector, re.I)) or []:
            tag.decompose()
        for tag in soup.select(selector):
            tag.decompose()

    # 2. TRY TO FIND MAIN ARTICLE (SMART SELECTORS)
    article = None
    candidates = [
        soup.find("article"),
        soup.find("div", class_=re.compile(r"content|article|story|post", re.I)),
        soup.find("div", id=re.compile(r"content|article|story", re.I)),
        soup.find("main"),
        soup.body
    ]
    for candidate in candidates:
        if candidate and len(candidate.get_text()) > 500:
            article = candidate
            break

    if not article:
        article = soup

    # 3. EXTRACT TEXT WITH BEST QUALITY
    text = article.get_text(separator="\n", strip=True)

    # 4. PROFESSIONAL CLEANING (REGEX POWER)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove common junk patterns
        if any(phrase in line.lower() for phrase in [
            "subscribe", "newsletter", "sign up", "advertisement", "read more", 
            "click here", "follow us", "share this", "related articles", "also read"
        ]):
            continue
        lines.append(line)

    cleaned = "\n".join(lines)

    # Remove extra whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)   # Max 2 newlines
    cleaned = re.sub(r'[ \t]{3,}', ' ', cleaned)   # Collapse spaces

    # FINAL: RETURN FULL RICH CONTENT
    return cleaned[:50000]  # 50,000 chars = perfect for Mistral AI

# BONUS: Optional — extract better title
def extract_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()
    return "No title found"