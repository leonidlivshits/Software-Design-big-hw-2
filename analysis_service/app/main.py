import asyncio
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import httpx
from fastapi.responses import Response
from app.config import settings
from .models import Base
from .schemas import AnalysisResult as AnalysisResultSchema
from .crud import get_analysis, create_analysis
from .analyzer import fetch_file, analyze_text, generate_wordcloud
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
async def analyze(file_id: int, db: Session = Depends(get_db)):
    existing = get_analysis(db, file_id)

    if existing and existing.wordcloud_url:
        return existing

    try:
        text = await fetch_file(file_id)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to fetch file")

    paragraphs, words, characters = await analyze_text(text)
    wordcloud_url = await generate_wordcloud(text)

    if existing:
        existing.paragraphs = paragraphs
        existing.words = words
        existing.characters = characters
        existing.wordcloud_url = wordcloud_url
        db.commit()
        db.refresh(existing)
        return existing

    result = create_analysis(db, file_id, paragraphs, words, characters, wordcloud_url)
    return result

@app.get("/analyze/{file_id}", response_model=AnalysisResultSchema)
async def get_result(file_id: int, db: Session = Depends(get_db)):
    result = get_analysis(db, file_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result



@app.get(
    "/analyze/{file_id}/wordcloud",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "PNG image of the word cloud",
        },
        404: {"description": "Analysis or wordcloud not found"},
        502: {"description": "Error fetching wordcloud image"},
    },
)
async def download_wordcloud(file_id: int, db: Session = Depends(get_db)):
    result = get_analysis(db, file_id)
    if not result or not result.wordcloud_url:
        raise HTTPException(status_code=404, detail="Wordcloud not available")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(result.wordcloud_url)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}")

    return Response(content=resp.content, media_type="image/png")