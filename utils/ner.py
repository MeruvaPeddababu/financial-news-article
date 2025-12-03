import spacy

nlp = spacy.load("en_core_web_lg")

TICKER_MAP = {
    "HDFC Bank": "HDFCBANK", "ICICI Bank": "ICICIBANK", "Reliance": "RELIANCE",
    "Tata Motors": "TATAMOTORS", "RBI": "RBI", "Reserve Bank of India": "RBI",
    "Axis Bank": "AXISBANK", "SBI": "SBIN", "State Bank of India": "SBIN"
}

def extract_entities(text: str):
    from models import NewsEntity
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        symbol = None
        if ent.text in TICKER_MAP:
            symbol = TICKER_MAP[ent.text]
        elif ent.label_ == "ORG" and any(bank in ent.text for bank in ["Bank", "Lenders"]):
            # heuristic
            pass
        entities.append(NewsEntity(text=ent.text, label=ent.label_, symbol=symbol))
    return entities