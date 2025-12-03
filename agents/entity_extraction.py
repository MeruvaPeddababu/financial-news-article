from utils.ner import extract_entities

def entity_extraction_agent(state):
    for news in state.processed_news:
        if not news.entities and news.cluster_id is not None:
            news.entities = extract_entities(news.title + " " + news.content)
    return state