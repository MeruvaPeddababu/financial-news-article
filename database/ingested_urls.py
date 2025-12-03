# database/ingested_urls.py – TRACKS EVERY URL + SESSION
import sqlite3
from datetime import datetime

DB_PATH = "ingested_urls.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingested (
            url TEXT PRIMARY KEY,
            session_id TEXT,
            ingested_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_url_already_ingested(url: str, session_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM ingested WHERE url = ? AND session_id = ?", (url, session_id))
    result = c.fetchone() is not None
    conn.close()
    return result

def mark_urls_ingested(urls: list, session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.executemany(
        "INSERT OR IGNORE INTO ingested (url, session_id, ingested_at) VALUES (?, ?, ?)",
        [(url, session_id, now) for url in urls]
    )
    conn.commit()
    conn.close()