# File: backend/app/models/db_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AnalysisRecord(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    email_risk = Column(Float)
    final_risk = Column(Float)
    classification = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    urls = relationship("URLAnalysisRecord", back_populates="analysis")

class URLAnalysisRecord(Base):
    __tablename__ = "url_analysis"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis.id"))
    url = Column(Text)
    ml_risk = Column(Float)
    reputation_risk = Column(Float)
    classification = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("AnalysisRecord", back_populates="urls")