"""
Pydantic schemas for API serialization
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, Union
from datetime import datetime
import json

class StatementBase(BaseModel):
    """Base statement schema"""
    cardholder_name: Optional[str] = None
    card_last_four: Optional[str] = None
    billing_period_start: Optional[datetime] = None
    billing_period_end: Optional[datetime] = None
    payment_due_date: Optional[datetime] = None
    total_amount_due: Optional[float] = None

class StatementCreate(StatementBase):
    """Schema for creating a statement"""
    filename: str
    file_path: str
    issuer: Optional[str] = None
    extraction_method: Optional[str] = None
    overall_confidence: Optional[float] = None
    extraction_steps: Optional[Union[Dict[str, Any], str]] = None
    llm_rationale: Optional[str] = None

class StatementUpdate(StatementBase):
    """Schema for updating a statement"""
    extraction_method: Optional[str] = None
    overall_confidence: Optional[float] = None
    extraction_steps: Optional[Union[Dict[str, Any], str]] = None
    llm_rationale: Optional[str] = None

class StatementResponse(StatementBase):
    """Schema for statement response"""
    id: int
    filename: str
    file_path: str
    issuer: Optional[str] = None
    extraction_method: Optional[str] = None
    overall_confidence: Optional[float] = None
    extraction_steps: Optional[Union[Dict[str, Any], str]] = None
    llm_rationale: Optional[str] = None
    is_processed: bool
    has_errors: bool
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @validator('extraction_steps', pre=True)
    def parse_extraction_steps(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return {}
        return v or {}
    
    class Config:
        from_attributes = True

class ExtractionResult(BaseModel):
    """Schema for extraction result"""
    cardholder_name: Optional[str] = None
    card_last_four: Optional[str] = None
    billing_period_start: Optional[datetime] = None
    billing_period_end: Optional[datetime] = None
    payment_due_date: Optional[datetime] = None
    total_amount_due: Optional[float] = None
    
    # Confidence scores for each field
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    
    # Overall extraction metadata
    overall_confidence: float = 0.0
    extraction_method: str = "unknown"
    extraction_steps: Dict[str, Any] = Field(default_factory=dict)
    llm_rationale: Optional[str] = None
    
    # Field-level rationale
    field_rationale: Dict[str, str] = Field(default_factory=dict)

class UploadResponse(BaseModel):
    """Schema for upload response"""
    statement_id: int
    filename: str
    extraction_result: ExtractionResult
    file_url: str
