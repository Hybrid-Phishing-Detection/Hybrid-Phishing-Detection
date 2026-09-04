# File: backend/app/schemas/analysis.py
from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    subject: str
    body: str

class URLAnalysisResult(BaseModel):
    url: str
    ml_risk: float
    reputation_risk: float
    classification: str

class AnalyzeResponse(BaseModel):
    email_risk: float
    classification: str
    urls: List[URLAnalysisResult]
    final_risk: float