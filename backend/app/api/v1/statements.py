"""
Statements API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import json

from app.models.database import get_db, Statement
from app.schemas.statement import StatementResponse, StatementUpdate

router = APIRouter()

@router.get("/statements", response_model=List[StatementResponse])
async def get_statements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    issuer: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of parsed statements"""
    
    query = db.query(Statement)
    
    if issuer:
        query = query.filter(Statement.issuer == issuer)
    
    statements = query.offset(skip).limit(limit).all()
    return statements

@router.get("/statements/{statement_id}", response_model=StatementResponse)
async def get_statement(statement_id: int, db: Session = Depends(get_db)):
    """Get a specific statement by ID"""
    
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    return statement

@router.put("/statements/{statement_id}", response_model=StatementResponse)
async def update_statement(
    statement_id: int,
    statement_update: StatementUpdate,
    db: Session = Depends(get_db)
):
    """Update a statement (manual correction)"""
    
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    # Update fields
    update_data = statement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(statement, field, value)
    
    statement.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(statement)
    
    return statement

@router.delete("/statements/{statement_id}")
async def delete_statement(statement_id: int, db: Session = Depends(get_db)):
    """Delete a statement"""
    
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    # Delete file
    import os
    if os.path.exists(statement.file_path):
        os.remove(statement.file_path)
    
    db.delete(statement)
    db.commit()
    
    return {"message": "Statement deleted successfully"}

@router.get("/statements/{statement_id}/reprocess")
async def reprocess_statement(
    statement_id: int,
    db: Session = Depends(get_db)
):
    """Reprocess a statement with updated extraction"""
    
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    try:
        from app.services.extractor import StatementExtractor
        
        extractor = StatementExtractor()
        extraction_result = await extractor.extract_from_pdf(statement.file_path, statement.issuer)
        
        # Update statement with new extraction results
        statement.cardholder_name = extraction_result["extracted_fields"].get("cardholder_name")
        statement.card_last_four = extraction_result["extracted_fields"].get("card_last_four")
        statement.billing_period_start = extraction_result["extracted_fields"].get("billing_period_start")
        statement.billing_period_end = extraction_result["extracted_fields"].get("billing_period_end")
        statement.payment_due_date = extraction_result["extracted_fields"].get("payment_due_date")
        statement.total_amount_due = extraction_result["extracted_fields"].get("total_amount_due")
        statement.extraction_method = extraction_result["extraction_method"]
        statement.overall_confidence = extraction_result["overall_confidence"]
        statement.extraction_steps = json.dumps(extraction_result["extraction_steps"])
        statement.llm_rationale = extraction_result["llm_rationale"]
        statement.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(statement)
        
        return {
            "message": "Statement reprocessed successfully",
            "statement": statement
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reprocessing failed: {str(e)}")

@router.get("/statements/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Get parsing statistics"""
    
    total_statements = db.query(Statement).count()
    processed_statements = db.query(Statement).filter(Statement.is_processed == True).count()
    error_statements = db.query(Statement).filter(Statement.has_errors == True).count()
    
    # Average confidence
    avg_confidence = db.query(Statement.overall_confidence).filter(
        Statement.overall_confidence.isnot(None)
    ).all()
    avg_confidence = sum([c[0] for c in avg_confidence]) / len(avg_confidence) if avg_confidence else 0.0
    
    # Issuer breakdown
    issuer_stats = db.query(Statement.issuer, func.count(Statement.id)).group_by(Statement.issuer).all()
    
    return {
        "total_statements": total_statements,
        "processed_statements": processed_statements,
        "error_statements": error_statements,
        "average_confidence": round(avg_confidence, 3),
        "issuer_breakdown": dict(issuer_stats)
    }
