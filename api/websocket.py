# api/websocket.py – CENTRAL ALERT SYSTEM (MUST EXIST)
from fastapi import WebSocket
from typing import List
from datetime import datetime
import json

# Global list of connected clients
connected_clients: List[WebSocket] = []

def send_alert(message: str, data: dict = None):
    """
    Send real-time alert to ALL connected WebSocket clients
    """
    alert_payload = {
        "type": "breaking_news",
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S"),
        "data": data or {}
    }
    
    for client in connected_clients[:]:
        try:
            client.send_text(json.dumps(alert_payload, ensure_ascii=False))
        except Exception:
            connected_clients.remove(client)