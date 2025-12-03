from database.vector_store import add_news
from database.structured_db import save_news

def storage_agent(state):
    for news in state.processed_news:
        if news.embedding and news.cluster_id is not None:
            add_news(news)
            save_news(news)
    return state