import asyncio
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import httpx

from app.config import settings
from .models import Base
from .schemas import AnalysisResult as AnalysisResultSchema
from .crud import get_analysis, create_analysis
from .analyzer import fetch_file, analyze_text
#from common.config import settings as common_settings

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)
engine = create_engine(DATABASE_URL, echo=settings.DEBUG, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analysis Service")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/analyze/{file_id}", response_model=AnalysisResultSchema)
async def analyze(file_id: int, db=Depends(get_db)):

    existing = get_analysis(db, file_id)
    if existing:
        return existing

    try:
        text = await fetch_file(file_id)
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Failed to fetch file")

    paragraphs, words, characters = await analyze_text(text)
    result = create_analysis(db, file_id, paragraphs, words, characters)
    return result

@app.get("/analyze/{file_id}", response_model=AnalysisResultSchema)
async def get_result(file_id: int, db=Depends(get_db)):
    result = get_analysis(db, file_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result