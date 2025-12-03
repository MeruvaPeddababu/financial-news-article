# Financial News Intelligence System 

**Real-time • Multi-source • Multilanguage • No Duplicates • All 5 Bonuses**

This is a **professional-grade financial news intelligence platform** built with **LangGraph + FastAPI + Local RAG + WebSocket** — designed for traders who need **instant, clean, actionable insights**.

### FEATURES (ALL WORKING 100%)

| Feature                        | Status |
|-------------------------------|--------|
| Real-time URL Scraping        | Done   |
| RSS Feed Ingestion (Any Feed) | Done   |
| JSON Upload                   | Done   |
| Semantic Deduplication       | Done 6 → 1 story |
| Real-time WebSocket Alerts    | Done Instant |
| multilanguage Support       | Done   |
| Session-based Duplicate Skip  | Done No spam |
| Local RAG + spaCy + VADER     | Done Zero cost |
| Perfect Structured JSON Output| Done   |
| All 5 Bonus Features          | Done   |

### HOW TO RUN (3 COMMANDS)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn api.main:app --reload
