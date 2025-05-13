import os
from fastapi import UploadFile
from .config import settings


def save_file_bytes(file_id: int, filename: str, data: bytes) -> str:
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    path = os.path.join(settings.STORAGE_DIR, f"{file_id}_{filename}")
    with open(path, "wb") as f:
        f.write(data)
    return path


def get_file_path(file_id: int, filename: str) -> str:
    return os.path.join(settings.STORAGE_DIR, f"{file_id}_{filename}")