from sqlalchemy.orm import Session
from .models import FileMeta as FileMetaModel


def create_file_meta(db: Session, filename: str, content_type: str, size: int):
    file_meta = FileMetaModel(
        filename=filename,
        content_type=content_type,
        size=size,
    )
    db.add(file_meta)
    db.commit()
    db.refresh(file_meta)
    return file_meta


def get_file_meta(db: Session, file_id: int):
    return db.query(FileMetaModel).filter(FileMetaModel.id == file_id).first()