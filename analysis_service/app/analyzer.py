from .schemas import BaseModel
import httpx
from app.config import settings

async def fetch_file(file_id: int) -> str:
    url = f"{settings.FILE_SERVICE_URL}/files/{file_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text

async def analyze_text(text: str):
    paragraphs = len([p for p in text.split("\n\n") if p.strip()])
    words = len(text.split())
    characters = len(text)
    return paragraphs, words, characters