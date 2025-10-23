"""
AI Provider abstraction for LLM integration
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def validate_extraction(
        self, 
        extracted_text: str, 
        candidate_fields: Dict[str, Any],
        issuer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate and normalize extracted fields using AI
        
        Args:
            extracted_text: Raw text extracted from PDF
            candidate_fields: Fields extracted by regex/OCR
            issuer: Credit card issuer (optional)
            
        Returns:
            Dict with validated fields, confidence scores, and rationale
        """
        pass

class MockProvider(AIProvider):
    """Mock AI provider for offline testing"""
    
    async def validate_extraction(
        self, 
        extracted_text: str, 
        candidate_fields: Dict[str, Any],
        issuer: Optional[str] = None
    ) -> Dict[str, Any]:
        """Mock validation that returns candidate fields with mock confidence"""
        
        # Mock confidence scores
        confidence_scores = {
            "cardholder_name": 0.85,
            "card_last_four": 0.95,
            "billing_period_start": 0.80,
            "billing_period_end": 0.80,
            "payment_due_date": 0.90,
            "total_amount_due": 0.88
        }
        
        # Mock rationale
        rationale = {
            "cardholder_name": "Extracted from statement header using regex pattern",
            "card_last_four": "Found in card number section with high confidence",
            "billing_period_start": "Parsed from billing period text",
            "billing_period_end": "Parsed from billing period text", 
            "payment_due_date": "Extracted from payment due section",
            "total_amount_due": "Found in total amount section with currency formatting"
        }
        
        return {
            "validated_fields": candidate_fields,
            "confidence_scores": confidence_scores,
            "overall_confidence": sum(confidence_scores.values()) / len(confidence_scores),
            "extraction_method": "mock_ai",
            "rationale": rationale,
            "llm_rationale": f"Mock AI validation completed for {issuer or 'unknown'} statement"
        }

class OpenAIProvider(AIProvider):
    """OpenAI GPT integration"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = None
        
    async def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self.client is None:
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self.client
    
    async def validate_extraction(
        self, 
        extracted_text: str, 
        candidate_fields: Dict[str, Any],
        issuer: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate extraction using OpenAI GPT"""
        
        client = await self._get_client()
        
        prompt = self._build_validation_prompt(extracted_text, candidate_fields, issuer)
        
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting and validating credit card statement information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content
            return self._parse_ai_response(result_text, candidate_fields)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to mock provider behavior
            mock_provider = MockProvider()
            return await mock_provider.validate_extraction(extracted_text, candidate_fields, issuer)
    
    def _build_validation_prompt(self, extracted_text: str, candidate_fields: Dict[str, Any], issuer: Optional[str]) -> str:
        """Build the validation prompt for the LLM"""
        
        return f"""
You are validating credit card statement extraction results. Please analyze the extracted text and candidate fields, then provide validated results.

EXTRACTED TEXT:
{extracted_text[:2000]}...

CANDIDATE FIELDS:
{json.dumps(candidate_fields, indent=2)}

ISSUER: {issuer or 'Unknown'}

Please validate each field and return a JSON response with this exact structure:
{{
    "validated_fields": {{
        "cardholder_name": "string or null",
        "card_last_four": "string or null", 
        "billing_period_start": "YYYY-MM-DD or null",
        "billing_period_end": "YYYY-MM-DD or null",
        "payment_due_date": "YYYY-MM-DD or null",
        "total_amount_due": "number or null"
    }},
    "confidence_scores": {{
        "cardholder_name": 0.0-1.0,
        "card_last_four": 0.0-1.0,
        "billing_period_start": 0.0-1.0,
        "billing_period_end": 0.0-1.0,
        "payment_due_date": 0.0-1.0,
        "total_amount_due": 0.0-1.0
    }},
    "rationale": {{
        "cardholder_name": "explanation",
        "card_last_four": "explanation",
        "billing_period_start": "explanation",
        "billing_period_end": "explanation", 
        "payment_due_date": "explanation",
        "total_amount_due": "explanation"
    }},
    "overall_confidence": 0.0-1.0,
    "extraction_method": "openai_validation",
    "llm_rationale": "Overall explanation of validation process"
}}

IMPORTANT:
- Return ONLY valid JSON
- Use ISO date format (YYYY-MM-DD) for dates
- Use numeric values for amounts (no currency symbols)
- Provide confidence scores between 0.0 and 1.0
- If a field cannot be validated, set it to null and confidence to 0.0
- Be conservative with confidence scores
"""
    
    def _parse_ai_response(self, response_text: str, fallback_fields: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response and handle errors"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
                
            json_text = response_text[start_idx:end_idx]
            result = json.loads(json_text)
            
            # Validate required fields
            required_fields = ["validated_fields", "confidence_scores", "rationale"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            return result
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse AI response: {e}")
            logger.error(f"Response text: {response_text}")
            
            # Return fallback with low confidence
            return {
                "validated_fields": fallback_fields,
                "confidence_scores": {k: 0.3 for k in fallback_fields.keys()},
                "overall_confidence": 0.3,
                "extraction_method": "openai_fallback",
                "rationale": {k: "AI validation failed, using fallback" for k in fallback_fields.keys()},
                "llm_rationale": f"AI validation failed: {str(e)}"
            }

def get_ai_provider() -> AIProvider:
    """Factory function to get the configured AI provider"""
    from app.core.config import settings
    
    if settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider(settings.OPENAI_API_KEY)
    elif settings.AI_PROVIDER == "anthropic" and settings.ANTHROPIC_API_KEY:
        # TODO: Implement Anthropic provider
        logger.warning("Anthropic provider not implemented, falling back to mock")
        return MockProvider()
    else:
        logger.info("Using mock AI provider")
        return MockProvider()
