from sqlalchemy.orm import Session
from .models import AnalysisResult


def get_analysis(db: Session, file_id: int):
    return db.query(AnalysisResult).filter(AnalysisResult.file_id == file_id).first()


def create_analysis(
    db: Session,
    file_id: int,
    paragraphs: int,
    words: int,
    characters: int,
    wordcloud_url: str | None
) -> AnalysisResult:
    result = AnalysisResult(
        file_id=file_id,
        paragraphs=paragraphs,
        words=words,
        characters=characters,
        wordcloud_url=wordcloud_url
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


