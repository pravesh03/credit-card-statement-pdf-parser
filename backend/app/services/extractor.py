"""
Main extraction service that orchestrates all extractors
"""

from typing import Dict, Any, Optional
import logging
from pathlib import Path

from app.extractors.regex_extractors import get_extractor
from app.extractors.ocr import HybridExtractor
from app.extractors.layout import SmartLayoutExtractor
from app.ai.ai_provider import get_ai_provider

logger = logging.getLogger(__name__)

class StatementExtractor:
    """Main extraction service"""
    
    def __init__(self):
        self.regex_extractor = None
        self.ocr_extractor = HybridExtractor()
        self.layout_extractor = SmartLayoutExtractor()
        self.ai_provider = get_ai_provider()
    
    async def extract_from_pdf(self, pdf_path: str, issuer: Optional[str] = None) -> Dict[str, Any]:
        """Extract fields from PDF using multiple methods"""
        try:
            # Step 1: Try layout-aware extraction first
            logger.info("Starting layout-aware extraction")
            layout_result = self.layout_extractor.extract_fields_with_layout(pdf_path)
            
            if layout_result["extracted_fields"]:
                # Use layout results as base
                candidate_fields = layout_result["extracted_fields"]
                extraction_method = "layout_based"
            else:
                # Fall back to regex extraction
                logger.info("Falling back to regex extraction")
                self.regex_extractor = get_extractor(issuer)
                regex_result = self.regex_extractor.extract(layout_result["extracted_text"])
                candidate_fields = regex_result["extracted_fields"]
                extraction_method = "regex_based"
            
            # Step 2: Use AI to validate and improve results
            logger.info("Validating with AI")
            ai_result = await self.ai_provider.validate_extraction(
                layout_result["extracted_text"],
                candidate_fields,
                issuer
            )
            
            # Step 3: Combine results
            final_result = self._combine_results(
                layout_result,
                regex_result if 'regex_result' in locals() else None,
                ai_result,
                extraction_method
            )
            
            return final_result
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return {
                "extracted_fields": {},
                "extraction_method": "failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0},
                "llm_rationale": f"Extraction failed: {str(e)}"
            }
    
    def _combine_results(
        self, 
        layout_result: Dict[str, Any], 
        regex_result: Optional[Dict[str, Any]], 
        ai_result: Dict[str, Any],
        extraction_method: str
    ) -> Dict[str, Any]:
        """Combine results from different extraction methods"""
        
        # Start with AI-validated fields
        final_fields = ai_result.get("validated_fields", {})
        final_confidence = ai_result.get("confidence_scores", {})
        
        # Add extraction steps
        extraction_steps = {
            "layout_extraction": layout_result.get("extraction_steps", {}),
            "ai_validation": ai_result.get("extraction_method", "unknown")
        }
        
        if regex_result:
            extraction_steps["regex_extraction"] = regex_result.get("extraction_steps", {})
        
        # Calculate overall confidence
        confidence_values = [v for v in final_confidence.values() if v > 0]
        overall_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0.0
        
        return {
            "extracted_fields": final_fields,
            "extraction_method": f"{extraction_method}_ai_validated",
            "extraction_steps": extraction_steps,
            "confidence_scores": final_confidence,
            "overall_confidence": overall_confidence,
            "llm_rationale": ai_result.get("llm_rationale", ""),
            "field_rationale": ai_result.get("rationale", {})
        }
    
    def extract_with_fallback(self, pdf_path: str, issuer: Optional[str] = None) -> Dict[str, Any]:
        """Extract with fallback methods (no AI)"""
        try:
            # Try layout extraction first
            layout_result = self.layout_extractor.extract_fields_with_layout(pdf_path)
            
            if layout_result["extracted_fields"]:
                return layout_result
            
            # Fall back to regex
            self.regex_extractor = get_extractor(issuer)
            regex_result = self.regex_extractor.extract(layout_result["extracted_text"])
            
            return {
                "extracted_fields": regex_result["extracted_fields"],
                "extraction_method": "regex_fallback",
                "extraction_steps": regex_result["extraction_steps"],
                "confidence_scores": regex_result["confidence_scores"],
                "overall_confidence": sum(regex_result["confidence_scores"].values()) / len(regex_result["confidence_scores"]),
                "llm_rationale": "AI validation not available, using regex fallback"
            }
            
        except Exception as e:
            logger.error(f"Fallback extraction failed: {e}")
            return {
                "extracted_fields": {},
                "extraction_method": "failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0},
                "llm_rationale": f"All extraction methods failed: {str(e)}"
            }
