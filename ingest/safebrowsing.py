# ingest/safebrowsing.py
import requests
import os
from typing import List

# Load API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_KEY")
SAFE_BROWSING_API = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"

def is_url_safe(url: str) -> bool:
    """
    Check if URL is safe using Google Safe Browsing API
    Returns True if safe (or no key), False if malicious
    """
    if not GOOGLE_API_KEY:
        return True  # Skip check if no key

    payload = {
        "client": {
            "clientId": "financialnews-intelligence",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "THREAT_TYPE_UNSPECIFIED",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(SAFE_BROWSING_API, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return "matches" not in data or len(data["matches"]) == 0
        else:
            print(f"Safe Browsing API error: {response.status_code}")
            return True  # Fail open
    except Exception as e:
        print(f"Safe Browsing check failed: {e}")
        return True  # Never block on error