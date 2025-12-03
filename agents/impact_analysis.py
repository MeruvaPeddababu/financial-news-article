from models import StockImpact, ImpactType

def impact_analysis_agent(state):
    for news in state.processed_news:
        if news.impacts or not news.entities:
            continue
        impacts = []
        for ent in news.entities:
            if ent.symbol and ent.symbol != "RBI":
                impacts.append(StockImpact(
                    symbol=ent.symbol,
                    company_name=ent.text,
                    confidence=1.0,
                    type=ImpactType.DIRECT,
                    reason="Direct mention"
                ))
        if any("rate" in news.content.lower() for _ in ["repo", "interest", "policy"]):
            impacts.append(StockImpact(symbol="NIFTY_BANK", company_name="Banking Sector", confidence=0.9, type=ImpactType.REGULATORY, reason="Rate sensitivity"))
        news.impacts = impacts or [StockImpact(symbol="UNKNOWN", company_name="None", confidence=0.0, type=ImpactType.THEMATIC, reason="No impact")]
    return state