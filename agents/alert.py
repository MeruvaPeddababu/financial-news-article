# agents/alert.py – FINAL WINNING VERSION (NO ERRORS)
from api.websocket import send_alert

def trigger_realtime_alert(news_item):
    """
    Sends real-time alert when NEW UNIQUE story is detected
    """
    # Fixed sentiment logic — no more TypeError!
    content_lower = news_item.content.lower()
    if any(word in content_lower for word in ["dividend", "growth", "profit", "buyback", "expansion"]):
        sentiment = "POSITIVE"
    elif any(word in content_lower for word in ["penalty", "hike", "loss", "downgrade", "fraud"]):
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    send_alert(
        message=f"NEW STORY: {news_item.title[:70]}...",
        data={
            "type": "breaking_news_alert",
            "title": news_item.title,
            "summary": (news_item.content[:300] + "...") if len(news_item.content) > 300 else news_item.content,
            "source": news_item.source,
            "url": news_item.url or "",
            "published_at": news_item.published_at.strftime("%Y-%m-%d %H:%M"),
            "entities": [e.text for e in news_item.entities],
            "impacted_stocks": [
                {
                    "symbol": imp.symbol,
                    "company": imp.company_name,
                    "confidence": round(imp.confidence, 2),
                    "type": imp.type,
                    "reason": imp.reason
                }
                for imp in news_item.impacts if imp.confidence > 0
            ],
            "sentiment": sentiment
        }
    )