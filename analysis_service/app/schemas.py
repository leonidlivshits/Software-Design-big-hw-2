from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AnalysisResult(BaseModel):
    id: int
    file_id: int
    paragraphs: int
    words: int
    characters: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)