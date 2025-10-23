"""
Database configuration and models
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings

# Database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Statement(Base):
    """Credit card statement model"""
    __tablename__ = "statements"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    issuer = Column(String, nullable=True)
    
    # Extracted fields
    cardholder_name = Column(String, nullable=True)
    card_last_four = Column(String, nullable=True)
    billing_period_start = Column(DateTime, nullable=True)
    billing_period_end = Column(DateTime, nullable=True)
    payment_due_date = Column(DateTime, nullable=True)
    total_amount_due = Column(Float, nullable=True)
    
    # Metadata
    extraction_method = Column(String, nullable=True)  # regex, ocr, llm
    overall_confidence = Column(Float, nullable=True)
    extraction_steps = Column(Text, nullable=True)  # JSON string
    llm_rationale = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_processed = Column(Boolean, default=False)
    has_errors = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
