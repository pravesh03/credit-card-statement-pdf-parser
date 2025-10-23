"""
Regex-based extractors for different credit card issuers
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RegexExtractor:
    """Base class for regex-based extraction"""
    
    def __init__(self, issuer: str):
        self.issuer = issuer.lower()
        self.patterns = self._get_patterns()
    
    def _get_patterns(self) -> Dict[str, str]:
        """Get regex patterns for the issuer"""
        patterns = {
            "hdfc": {
                "cardholder_name": r"(?:Name|Cardholder|Account Holder)[\s:]*([A-Za-z\s\.]+)",
                "card_last_four": r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                "billing_period": r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "payment_due_date": r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "total_amount_due": r"(?:Total Amount Due|Amount Due|Outstanding)[\s:]*[₹$]?\s*([\d,]+\.?\d*)"
            },
            "sbi": {
                "cardholder_name": r"(?:Cardholder Name|Name)[\s:]*([A-Za-z\s\.]+)",
                "card_last_four": r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                "billing_period": r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "payment_due_date": r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "total_amount_due": r"(?:Total Amount Due|Amount Due)[\s:]*[₹$]?\s*([\d,]+\.?\d*)"
            },
            "icici": {
                "cardholder_name": r"(?:Cardholder Name|Name)[\s:]*([A-Za-z\s\.]+)",
                "card_last_four": r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                "billing_period": r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "payment_due_date": r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "total_amount_due": r"(?:Total Amount Due|Amount Due)[\s:]*[₹$]?\s*([\d,]+\.?\d*)"
            },
            "axis": {
                "cardholder_name": r"(?:Cardholder Name|Name)[\s:]*([A-Za-z\s\.]+)",
                "card_last_four": r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                "billing_period": r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "payment_due_date": r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "total_amount_due": r"(?:Total Amount Due|Amount Due)[\s:]*[₹$]?\s*([\d,]+\.?\d*)"
            },
            "citibank": {
                "cardholder_name": r"(?:Cardholder Name|Name)[\s:]*([A-Za-z\s\.]+)",
                "card_last_four": r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                "billing_period": r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "payment_due_date": r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                "total_amount_due": r"(?:Total Amount Due|Amount Due)[\s:]*[₹$]?\s*([\d,]+\.?\d*)"
            }
        }
        
        return patterns.get(self.issuer, patterns["hdfc"])  # Default to HDFC patterns
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract fields using regex patterns"""
        results = {}
        extraction_steps = {}
        
        # Clean and normalize text
        text = self._clean_text(text)
        
        for field, pattern in self.patterns.items():
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    if field == "billing_period":
                        # Special handling for billing period (two dates)
                        start_date, end_date = match.groups()
                        results["billing_period_start"] = self._parse_date(start_date)
                        results["billing_period_end"] = self._parse_date(end_date)
                        extraction_steps[field] = f"Matched pattern: {pattern}"
                    elif field == "total_amount_due":
                        # Parse amount
                        amount_str = match.group(1).replace(",", "")
                        results[field] = float(amount_str)
                        extraction_steps[field] = f"Matched pattern: {pattern}"
                    elif field in ["payment_due_date"]:
                        # Parse date fields
                        date_str = match.group(1).strip()
                        results[field] = self._parse_date(date_str)
                        extraction_steps[field] = f"Matched pattern: {pattern}"
                    else:
                        results[field] = match.group(1).strip()
                        extraction_steps[field] = f"Matched pattern: {pattern}"
                else:
                    results[field] = None
                    extraction_steps[field] = f"No match for pattern: {pattern}"
            except Exception as e:
                logger.error(f"Error extracting {field}: {e}")
                results[field] = None
                extraction_steps[field] = f"Error: {str(e)}"
        
        return {
            "extracted_fields": results,
            "extraction_steps": extraction_steps,
            "extraction_method": f"regex_{self.issuer}",
            "confidence_scores": self._calculate_confidence_scores(results)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for better regex matching"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\.,\-\/₹$]', '', text)
        return text.strip()
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string in various formats"""
        if not date_str:
            return None
            
        date_formats = [
            "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
            "%d/%m/%y", "%d-%m-%y", "%d.%m.%y",
            "%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y",
            "%Y-%m-%d"
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str.strip(), fmt)
                # Convert to ISO format string for Pydantic
                return parsed_date
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def _calculate_confidence_scores(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores based on extraction success"""
        confidence_scores = {}
        
        for field, value in results.items():
            if value is not None:
                if field in ["cardholder_name", "card_last_four"]:
                    confidence_scores[field] = 0.8  # High confidence for text fields
                elif field in ["billing_period_start", "billing_period_end", "payment_due_date"]:
                    confidence_scores[field] = 0.7  # Medium confidence for dates
                elif field == "total_amount_due":
                    confidence_scores[field] = 0.9  # High confidence for amounts
                else:
                    confidence_scores[field] = 0.6  # Default confidence
            else:
                confidence_scores[field] = 0.0
        
        return confidence_scores

class UniversalExtractor(RegexExtractor):
    """Universal extractor that tries multiple patterns"""
    
    def __init__(self):
        super().__init__("universal")
        self.universal_patterns = {
            "cardholder_name": [
                r"(?:Name|Cardholder|Account Holder)[\s:]*([A-Za-z\s\.]+)",
                r"([A-Z][a-z]+\s+[A-Z][a-z]+)",  # Simple name pattern
            ],
            "card_last_four": [
                r"(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})",
                r"\*{4,}\s*(\d{4})",  # Simple pattern
            ],
            "billing_period": [
                r"(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"(?:Due|Payment Due)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_amount_due": [
                r"(?:Total Amount Due|Amount Due|Outstanding)[\s:]*[₹$]?\s*([\d,]+\.?\d*)",
                r"(?:Total|Amount)[\s:]*[₹$]?\s*([\d,]+\.?\d*)",
            ]
        }
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract using universal patterns"""
        results = {}
        extraction_steps = {}
        
        text = self._clean_text(text)
        
        for field, patterns in self.universal_patterns.items():
            best_match = None
            best_pattern = None
            
            for pattern in patterns:
                try:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        best_match = match
                        best_pattern = pattern
                        break  # Use first match
                except Exception as e:
                    logger.error(f"Error with pattern {pattern}: {e}")
                    continue
            
            if best_match:
                if field == "billing_period":
                    start_date, end_date = best_match.groups()
                    results["billing_period_start"] = self._parse_date(start_date)
                    results["billing_period_end"] = self._parse_date(end_date)
                    extraction_steps[field] = f"Matched pattern: {best_pattern}"
                elif field == "total_amount_due":
                    amount_str = best_match.group(1).replace(",", "")
                    results[field] = float(amount_str)
                    extraction_steps[field] = f"Matched pattern: {best_pattern}"
                else:
                    results[field] = best_match.group(1).strip()
                    extraction_steps[field] = f"Matched pattern: {best_pattern}"
            else:
                results[field] = None
                extraction_steps[field] = "No pattern matched"
        
        return {
            "extracted_fields": results,
            "extraction_steps": extraction_steps,
            "extraction_method": "universal_regex",
            "confidence_scores": self._calculate_confidence_scores(results)
        }

def get_extractor(issuer: Optional[str] = None) -> RegexExtractor:
    """Factory function to get appropriate extractor"""
    if issuer:
        return RegexExtractor(issuer)
    else:
        return UniversalExtractor()
