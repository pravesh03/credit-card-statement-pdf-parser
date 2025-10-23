"""
Upload API endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
import logging
import json
from datetime import datetime

from app.models.database import get_db, Statement
from app.schemas.statement import StatementCreate, UploadResponse, ExtractionResult
from app.services.extractor import StatementExtractor
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_statement(
    file: UploadFile = File(...),
    issuer: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload and parse a credit card statement PDF"""
    
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save file
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract fields
        extractor = StatementExtractor()
        extraction_result = await extractor.extract_from_pdf(file_path, issuer)
        
        # Create database record
        statement_data = StatementCreate(
            filename=file.filename,
            file_path=file_path,
            issuer=issuer,
            cardholder_name=extraction_result["extracted_fields"].get("cardholder_name"),
            card_last_four=extraction_result["extracted_fields"].get("card_last_four"),
            billing_period_start=extraction_result["extracted_fields"].get("billing_period_start"),
            billing_period_end=extraction_result["extracted_fields"].get("billing_period_end"),
            payment_due_date=extraction_result["extracted_fields"].get("payment_due_date"),
            total_amount_due=extraction_result["extracted_fields"].get("total_amount_due"),
            extraction_method=extraction_result["extraction_method"],
            overall_confidence=extraction_result["overall_confidence"],
            extraction_steps=json.dumps(extraction_result["extraction_steps"]),  # Convert dict to JSON string
            llm_rationale=extraction_result["llm_rationale"]
        )
        
        # Save to database
        db_statement = Statement(**statement_data.dict())
        db.add(db_statement)
        db.commit()
        db.refresh(db_statement)
        
        # Prepare response
        extraction_result_schema = ExtractionResult(
            cardholder_name=extraction_result["extracted_fields"].get("cardholder_name"),
            card_last_four=extraction_result["extracted_fields"].get("card_last_four"),
            billing_period_start=extraction_result["extracted_fields"].get("billing_period_start"),
            billing_period_end=extraction_result["extracted_fields"].get("billing_period_end"),
            payment_due_date=extraction_result["extracted_fields"].get("payment_due_date"),
            total_amount_due=extraction_result["extracted_fields"].get("total_amount_due"),
            confidence_scores=extraction_result["confidence_scores"],
            overall_confidence=extraction_result["overall_confidence"],
            extraction_method=extraction_result["extraction_method"],
            extraction_steps=extraction_result["extraction_steps"],
            llm_rationale=extraction_result["llm_rationale"],
            field_rationale=extraction_result.get("field_rationale", {})
        )
        
        return UploadResponse(
            statement_id=db_statement.id,
            filename=file.filename,
            extraction_result=extraction_result_schema,
            file_url=f"http://localhost:8000/uploads/{filename}"
        )
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload-batch")
async def upload_batch(
    files: list[UploadFile] = File(...),
    issuer: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload multiple PDF files"""
    
    results = []
    errors = []
    
    for file in files:
        try:
            result = await upload_statement(file, issuer, db)
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "successful_uploads": len(results),
        "failed_uploads": len(errors),
        "results": results,
        "errors": errors
    }
