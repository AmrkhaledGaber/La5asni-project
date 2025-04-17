from pydantic import BaseModel
from typing import List

class AnalysisResponse(BaseModel):
    summary: str
    key_points: List[str]
    training_modules: List[str]
    num_pages: int
    useful_text_ratio: float
    num_key_points: int
    estimated_minutes_per_module: List[int]
