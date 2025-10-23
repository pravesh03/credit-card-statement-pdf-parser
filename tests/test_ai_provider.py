"""
Tests for AI provider modules
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.ai.ai_provider import MockProvider, OpenAIProvider, get_ai_provider

class TestMockProvider:
    """Test mock AI provider"""
    
    @pytest.mark.asyncio
    async def test_mock_provider_validation(self):
        """Test mock provider validation"""
        provider = MockProvider()
        
        extracted_text = "Sample credit card statement text"
        candidate_fields = {
            "cardholder_name": "John Doe",
            "card_last_four": "1234",
            "total_amount_due": 1000.0
        }
        
        result = await provider.validate_extraction(extracted_text, candidate_fields, "hdfc")
        
        assert "validated_fields" in result
        assert "confidence_scores" in result
        assert "overall_confidence" in result
        assert "extraction_method" in result
        assert "rationale" in result
        assert "llm_rationale" in result
        
        # Check that validated fields match candidate fields
        assert result["validated_fields"]["cardholder_name"] == "John Doe"
        assert result["validated_fields"]["card_last_four"] == "1234"
        assert result["validated_fields"]["total_amount_due"] == 1000.0
        
        # Check confidence scores
        assert all(0 <= score <= 1 for score in result["confidence_scores"].values())
        assert result["overall_confidence"] > 0
    
    @pytest.mark.asyncio
    async def test_mock_provider_with_none_values(self):
        """Test mock provider with None values"""
        provider = MockProvider()
        
        extracted_text = "Sample text"
        candidate_fields = {
            "cardholder_name": None,
            "card_last_four": None,
            "total_amount_due": None
        }
        
        result = await provider.validate_extraction(extracted_text, candidate_fields)
        
        assert result["validated_fields"]["cardholder_name"] is None
        assert result["validated_fields"]["card_last_four"] is None
        assert result["validated_fields"]["total_amount_due"] is None

class TestOpenAIProvider:
    """Test OpenAI provider"""
    
    def test_openai_provider_initialization(self):
        """Test OpenAI provider initialization"""
        provider = OpenAIProvider("test-api-key")
        assert provider.api_key == "test-api-key"
        assert provider.model == "gpt-3.5-turbo"
    
    def test_openai_provider_with_custom_model(self):
        """Test OpenAI provider with custom model"""
        provider = OpenAIProvider("test-api-key", "gpt-4")
        assert provider.model == "gpt-4"
    
    def test_build_validation_prompt(self):
        """Test prompt building"""
        provider = OpenAIProvider("test-api-key")
        
        extracted_text = "Sample statement text"
        candidate_fields = {"cardholder_name": "John Doe"}
        issuer = "hdfc"
        
        prompt = provider._build_validation_prompt(extracted_text, candidate_fields, issuer)
        
        assert "EXTRACTED TEXT:" in prompt
        assert "CANDIDATE FIELDS:" in prompt
        assert "ISSUER: hdfc" in prompt
        assert "JSON response" in prompt
        assert "validated_fields" in prompt
        assert "confidence_scores" in prompt
    
    def test_parse_ai_response_valid_json(self):
        """Test parsing valid AI response"""
        provider = OpenAIProvider("test-api-key")
        
        response_text = '''
        {
            "validated_fields": {
                "cardholder_name": "John Doe",
                "card_last_four": "1234"
            },
            "confidence_scores": {
                "cardholder_name": 0.9,
                "card_last_four": 0.95
            },
            "rationale": {
                "cardholder_name": "Found in header",
                "card_last_four": "Extracted from card number"
            },
            "overall_confidence": 0.925,
            "extraction_method": "openai_validation",
            "llm_rationale": "Successfully validated"
        }
        '''
        
        fallback_fields = {"cardholder_name": "John Doe"}
        result = provider._parse_ai_response(response_text, fallback_fields)
        
        assert result["validated_fields"]["cardholder_name"] == "John Doe"
        assert result["validated_fields"]["card_last_four"] == "1234"
        assert result["confidence_scores"]["cardholder_name"] == 0.9
        assert result["overall_confidence"] == 0.925
        assert result["extraction_method"] == "openai_validation"
    
    def test_parse_ai_response_invalid_json(self):
        """Test parsing invalid AI response"""
        provider = OpenAIProvider("test-api-key")
        
        response_text = "This is not valid JSON"
        fallback_fields = {"cardholder_name": "John Doe"}
        
        result = provider._parse_ai_response(response_text, fallback_fields)
        
        assert result["validated_fields"]["cardholder_name"] == "John Doe"
        assert result["overall_confidence"] == 0.3
        assert result["extraction_method"] == "openai_fallback"
        assert "AI validation failed" in result["llm_rationale"]
    
    def test_parse_ai_response_missing_fields(self):
        """Test parsing response with missing required fields"""
        provider = OpenAIProvider("test-api-key")
        
        response_text = '{"validated_fields": {"cardholder_name": "John"}}'
        fallback_fields = {"cardholder_name": "John Doe"}
        
        result = provider._parse_ai_response(response_text, fallback_fields)
        
        assert result["validated_fields"]["cardholder_name"] == "John Doe"
        assert result["overall_confidence"] == 0.3
        assert result["extraction_method"] == "openai_fallback"

class TestAIProviderFactory:
    """Test AI provider factory function"""
    
    def test_get_mock_provider_default(self):
        """Test getting mock provider by default"""
        provider = get_ai_provider()
        assert isinstance(provider, MockProvider)
    
    @patch('app.ai.ai_provider.settings')
    def test_get_openai_provider(self, mock_settings):
        """Test getting OpenAI provider"""
        mock_settings.AI_PROVIDER = "openai"
        mock_settings.OPENAI_API_KEY = "test-key"
        
        provider = get_ai_provider()
        assert isinstance(provider, OpenAIProvider)
        assert provider.api_key == "test-key"
    
    @patch('app.ai.ai_provider.settings')
    def test_get_mock_provider_when_openai_key_missing(self, mock_settings):
        """Test getting mock provider when OpenAI key is missing"""
        mock_settings.AI_PROVIDER = "openai"
        mock_settings.OPENAI_API_KEY = ""
        
        provider = get_ai_provider()
        assert isinstance(provider, MockProvider)
    
    @patch('app.ai.ai_provider.settings')
    def test_get_mock_provider_when_anthropic_not_implemented(self, mock_settings):
        """Test getting mock provider when Anthropic is not implemented"""
        mock_settings.AI_PROVIDER = "anthropic"
        mock_settings.ANTHROPIC_API_KEY = "test-key"
        
        provider = get_ai_provider()
        assert isinstance(provider, MockProvider)

class TestIntegration:
    """Integration tests for AI providers"""
    
    @pytest.mark.asyncio
    async def test_mock_provider_integration(self):
        """Test mock provider with realistic data"""
        provider = MockProvider()
        
        extracted_text = """
        HDFC BANK LIMITED
        Credit Card Statement
        
        Name: JOHN DOE
        Card No: **** **** **** 1234
        
        Statement Period: 01/11/2023 to 30/11/2023
        Payment Due Date: 15/12/2023
        
        Total Amount Due: ₹7,549.00
        """
        
        candidate_fields = {
            "cardholder_name": "JOHN DOE",
            "card_last_four": "1234",
            "billing_period_start": "2023-11-01",
            "billing_period_end": "2023-11-30",
            "payment_due_date": "2023-12-15",
            "total_amount_due": 7549.0
        }
        
        result = await provider.validate_extraction(extracted_text, candidate_fields, "hdfc")
        
        # Verify all required fields are present
        required_fields = ["validated_fields", "confidence_scores", "overall_confidence", 
                          "extraction_method", "rationale", "llm_rationale"]
        for field in required_fields:
            assert field in result
        
        # Verify confidence scores are reasonable
        assert 0.5 <= result["overall_confidence"] <= 1.0
        
        # Verify extraction method
        assert result["extraction_method"] == "mock_ai"
