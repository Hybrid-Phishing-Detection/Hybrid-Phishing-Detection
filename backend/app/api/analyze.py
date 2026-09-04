# File: backend/app/api/analyze.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse, URLAnalysisResult
from app.services.url_analyzer import extract_urls, url_ml_analyzer
from app.services.email_analyzer import email_analyzer
from app.services.reputation import get_reputation_provider
from app.services.risk_engine import calculate_final_risk
from app.database import get_db
from app.models.db_models import AnalysisRecord, URLAnalysisRecord

router = APIRouter()
reputation_provider = get_reputation_provider()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(request: AnalyzeRequest, db: Session = Depends(get_db)):
    email_risk = email_analyzer.analyze(request.subject, request.body)
    
    # 제목과 본문을 병합하여 URL 추출 대상을 확장합니다.
    full_text = f"{request.subject} {request.body}"
    extracted_urls = extract_urls(full_text)
    
    urls_result = []
    url_final_risks = []
    
    for url in extracted_urls:
        ml_risk = url_ml_analyzer.analyze(url)
        rep_risk = reputation_provider.check_url(url)
        
        url_final_risk = (ml_risk * 0.4) + (rep_risk * 0.6)
        url_final_risks.append(url_final_risk)
        
        url_class = "high" if url_final_risk >= 0.7 else ("low" if url_final_risk < 0.3 else "medium")
        
        urls_result.append(URLAnalysisResult(
            url=url,
            ml_risk=ml_risk,
            reputation_risk=rep_risk,
            classification=url_class
        ))
        
    final_risk, classification = calculate_final_risk(email_risk, url_final_risks)
    
    db_analysis = AnalysisRecord(
        subject=request.subject,
        body=request.body,
        email_risk=email_risk,
        final_risk=final_risk,
        classification=classification.lower()
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    for u_res in urls_result:
        db_url = URLAnalysisRecord(
            analysis_id=db_analysis.id,
            url=u_res.url,
            ml_risk=u_res.ml_risk,
            reputation_risk=u_res.reputation_risk,
            classification=u_res.classification
        )
        db.add(db_url)
    db.commit()
    
    return AnalyzeResponse(
        email_risk=email_risk,
        classification=classification.lower(),
        urls=urls_result,
        final_risk=final_risk
    )