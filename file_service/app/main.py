import os
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from common.db import get_db, engine
from .models import Base
from .schemas import FileMeta as FileMetaSchema
from . import crud, storage, config


Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Service")


@app.post("/files/", response_model=FileMetaSchema)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in config.settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    data = file.file.read()
    size = len(data)
    if size > config.settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    meta = crud.create_file_meta(db, filename, file.content_type, size)
    storage.save_file_bytes(meta.id, filename, data)

    return meta


@app.get("/files/{file_id}", response_model=FileMetaSchema)
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
):
    meta = crud.get_file_meta(db, file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")

    path = storage.get_file_path(file_id, meta.filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File missing on disk")

    return FileResponse(path=path, media_type=meta.content_type, filename=meta.filename)