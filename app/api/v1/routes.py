from fastapi import APIRouter, UploadFile, File
from app.services.parser import extract_text
from app.services.analyzer import analyze_document
from app.models.schemas import AnalysisResponse
from app.services.database import save_analysis  # ✅ import the save function
from datetime import datetime

router = APIRouter()

@router.post("/analyze/", response_model=AnalysisResponse)
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    extracted = extract_text(file.filename, content)
    result = analyze_document(extracted["text"])
    return result



