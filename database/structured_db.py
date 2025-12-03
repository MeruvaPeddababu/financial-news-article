# database/structured_db.py
from sqlalchemy import create_engine, Column, String, JSON, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import ProcessedNews
from datetime import datetime
import json

engine = create_engine("sqlite:///news.db", future=True)
Base = declarative_base()

class NewsRecord(Base):
    __tablename__ = "news"
    id = Column(String, primary_key=True)
    data = Column(JSON)

# Create table if not exists
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def save_news(news: ProcessedNews):
    session = SessionLocal()
    try:
        # Convert datetime → ISO string before saving
        data_to_save = news.dict()
        if isinstance(data_to_save.get("published_at"), datetime):
            data_to_save["published_at"] = data_to_save["published_at"].isoformat()

        record = NewsRecord(id=news.id, data=data_to_save)
        session.merge(record)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"DB Save Error: {e}")
    finally:
        session.close()