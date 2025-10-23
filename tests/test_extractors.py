"""
Tests for extraction modules
"""

import pytest
import tempfile
import os
from datetime import datetime
from app.extractors.regex_extractors import RegexExtractor, UniversalExtractor
from app.extractors.ocr import OCRExtractor, HybridExtractor
from app.extractors.layout import LayoutExtractor, SmartLayoutExtractor

class TestRegexExtractors:
    """Test regex-based extractors"""
    
    def test_hdfc_extractor(self):
        """Test HDFC-specific extraction"""
        extractor = RegexExtractor("hdfc")
        
        # Sample HDFC statement text
        text = """
        HDFC BANK LIMITED
        Credit Card Statement
        
        Name: JOHN DOE
        Card No: **** **** **** 1234
        
        Statement Period: 01/11/2023 to 30/11/2023
        Payment Due Date: 15/12/2023
        
        Total Amount Due: ₹7,549.00
        """
        
        result = extractor.extract(text)
        
        assert result["extracted_fields"]["cardholder_name"] == "JOHN DOE"
        assert result["extracted_fields"]["card_last_four"] == "1234"
        assert result["extracted_fields"]["total_amount_due"] == 7549.0
        assert result["extraction_method"] == "regex_hdfc"
    
    def test_sbi_extractor(self):
        """Test SBI-specific extraction"""
        extractor = RegexExtractor("sbi")
        
        text = """
        STATE BANK OF INDIA
        Credit Card Statement
        
        Cardholder Name: JANE SMITH
        Card Number: **** **** **** 5678
        
        Billing Period: 01-11-2023 to 30-11-2023
        Due Date: 15-12-2023
        
        Amount Due: ₹3,450.00
        """
        
        result = extractor.extract(text)
        
        assert result["extracted_fields"]["cardholder_name"] == "JANE SMITH"
        assert result["extracted_fields"]["card_last_four"] == "5678"
        assert result["extracted_fields"]["total_amount_due"] == 3450.0
    
    def test_universal_extractor(self):
        """Test universal extractor"""
        extractor = UniversalExtractor()
        
        text = """
        Credit Card Statement
        
        Name: ALICE JOHNSON
        Card No: **** **** **** 9012
        
        Statement Period: 01.11.2023 to 30.11.2023
        Payment Due Date: 15.12.2023
        
        Total Amount Due: ₹4,428.00
        """
        
        result = extractor.extract(text)
        
        assert result["extracted_fields"]["cardholder_name"] == "ALICE JOHNSON"
        assert result["extracted_fields"]["card_last_four"] == "9012"
        assert result["extracted_fields"]["total_amount_due"] == 4428.0
        assert result["extraction_method"] == "universal_regex"
    
    def test_confidence_scores(self):
        """Test confidence score calculation"""
        extractor = RegexExtractor("hdfc")
        
        text = """
        Name: JOHN DOE
        Card No: **** **** **** 1234
        Total Amount Due: ₹7,549.00
        """
        
        result = extractor.extract(text)
        confidence_scores = result["confidence_scores"]
        
        assert confidence_scores["cardholder_name"] > 0
        assert confidence_scores["card_last_four"] > 0
        assert confidence_scores["total_amount_due"] > 0
        assert confidence_scores["billing_period_start"] == 0.0  # Not found
        assert confidence_scores["payment_due_date"] == 0.0  # Not found

class TestOCRExtractor:
    """Test OCR extraction"""
    
    def test_ocr_extractor_initialization(self):
        """Test OCR extractor initialization"""
        extractor = OCRExtractor()
        assert extractor.language == "eng"
        assert extractor.confidence_threshold == 0.6
    
    def test_hybrid_extractor_initialization(self):
        """Test hybrid extractor initialization"""
        extractor = HybridExtractor()
        assert extractor.ocr_extractor is not None

class TestLayoutExtractor:
    """Test layout-aware extraction"""
    
    def test_layout_extractor_initialization(self):
        """Test layout extractor initialization"""
        extractor = LayoutExtractor()
        assert extractor.table_settings is not None
    
    def test_smart_layout_extractor_initialization(self):
        """Test smart layout extractor initialization"""
        extractor = SmartLayoutExtractor()
        assert extractor is not None

class TestIntegration:
    """Integration tests"""
    
    def test_extraction_pipeline(self):
        """Test complete extraction pipeline"""
        # This would test the full pipeline with actual PDF files
        # For now, we'll test the components individually
        pass
    
    def test_error_handling(self):
        """Test error handling in extractors"""
        extractor = RegexExtractor("hdfc")
        
        # Test with empty text
        result = extractor.extract("")
        assert result["extracted_fields"]["cardholder_name"] is None
        assert result["extraction_method"] == "regex_hdfc"
        
        # Test with malformed text
        result = extractor.extract("Invalid text without patterns")
        assert result["extracted_fields"]["cardholder_name"] is None
