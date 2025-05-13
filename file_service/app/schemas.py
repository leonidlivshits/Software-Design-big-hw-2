from datetime import datetime
from pydantic import BaseModel


class FileMeta(BaseModel):
    id: int
    filename: str
    content_type: str
    size: int
    upload_time: datetime

    class Config:
        orm_mode = True