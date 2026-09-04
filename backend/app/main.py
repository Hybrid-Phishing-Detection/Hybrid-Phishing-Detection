# File: backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze
from app.database import engine, Base

# 데이터베이스 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hybrid Phishing Detection API",
    description="이메일 텍스트, URL 구조, 외부 Reputation을 결합한 피싱 탐지 시스템 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["Analysis"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}