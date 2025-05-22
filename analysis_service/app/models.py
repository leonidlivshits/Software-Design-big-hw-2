from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func

Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, nullable=False, unique=True)
    paragraphs = Column(Integer, nullable=False)
    words = Column(Integer, nullable=False)
    characters = Column(Integer, nullable=False)
    wordcloud_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())