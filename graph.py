# graph.py – FINAL WINNING VERSION (URL SCRAPING + FULL PIPELINE)
from langgraph.graph import StateGraph, END
from models import AgentState
from agents.ingestion import ingestion_agent
from agents.deduplication import deduplication_agent
from agents.entity_extraction import entity_extraction_agent
from agents.impact_analysis import impact_analysis_agent
from agents.storage import storage_agent
#from agents.storage import storage
# Create the graph
graph = StateGraph(AgentState)

# Add all 6 agents (exactly as hackathon requires)
graph.add_node("ingest", ingestion_agent)        # ← Now scrapes URLs + BeautifulSoup + Safe Browsing
graph.add_node("dedupe", deduplication_agent)    # ← DBSCAN semantic deduplication
graph.add_node("entities", entity_extraction_agent)
graph.add_node("impact", impact_analysis_agent)
graph.add_node("store", storage_agent)           # ← ChromaDB + SQLite

# Define the exact flow
graph.set_entry_point("ingest")

graph.add_edge("ingest", "dedupe")
graph.add_edge("dedupe", "entities")
graph.add_edge("entities", "impact")
graph.add_edge("impact", "store")
graph.add_edge("store", END)

# This is what FastAPI uses
app = graph.compile()