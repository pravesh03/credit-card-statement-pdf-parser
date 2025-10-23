"""
Layout-aware text extraction using pdfplumber
"""

import pdfplumber
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LayoutExtractor:
    """Layout-aware text extraction using pdfplumber"""
    
    def __init__(self):
        self.table_settings = {
            "vertical_strategy": "lines_strict",
            "horizontal_strategy": "lines_strict",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 1,
            "min_words_horizontal": 1,
        }
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text with layout information"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_text = ""
                layout_info = {}
                extraction_steps = {}
                
                for page_num, page in enumerate(pdf.pages):
                    # Extract text with layout
                    page_text = self._extract_page_text(page)
                    all_text += page_text + "\n"
                    
                    # Extract tables
                    tables = self._extract_tables(page)
                    if tables:
                        layout_info[f"page_{page_num}_tables"] = tables
                    
                    # Extract layout information
                    layout_info[f"page_{page_num}_layout"] = self._analyze_layout(page)
                    
                    extraction_steps[f"page_{page_num}"] = f"Layout extraction (text: {len(page_text)} chars)"
                
                return {
                    "extracted_text": all_text.strip(),
                    "layout_info": layout_info,
                    "extraction_method": "layout_pdfplumber",
                    "extraction_steps": extraction_steps,
                    "confidence_scores": {"overall": 0.8}
                }
                
        except Exception as e:
            logger.error(f"Layout extraction failed: {e}")
            return {
                "extracted_text": "",
                "layout_info": {},
                "extraction_method": "layout_failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0}
            }
    
    def _extract_page_text(self, page) -> str:
        """Extract text from a page with layout awareness"""
        try:
            # Get text with character positioning
            chars = page.chars
            
            # Sort characters by position (top to bottom, left to right)
            chars_sorted = sorted(chars, key=lambda c: (c['top'], c['x0']))
            
            # Group characters into lines
            lines = []
            current_line = []
            current_y = None
            
            for char in chars_sorted:
                if current_y is None or abs(char['top'] - current_y) < 5:  # Same line
                    current_line.append(char)
                    current_y = char['top']
                else:  # New line
                    if current_line:
                        line_text = ''.join([c['text'] for c in current_line])
                        lines.append(line_text.strip())
                    current_line = [char]
                    current_y = char['top']
            
            # Add last line
            if current_line:
                line_text = ''.join([c['text'] for c in current_line])
                lines.append(line_text.strip())
            
            return '\n'.join(lines)
            
        except Exception as e:
            logger.error(f"Page text extraction failed: {e}")
            return page.extract_text() or ""
    
    def _extract_tables(self, page) -> List[Dict[str, Any]]:
        """Extract tables from a page"""
        try:
            tables = page.extract_tables(table_settings=self.table_settings)
            table_data = []
            
            for table in tables:
                if table and len(table) > 1:  # At least header + 1 row
                    table_data.append({
                        "rows": len(table),
                        "columns": len(table[0]) if table[0] else 0,
                        "data": table
                    })
            
            return table_data
            
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
            return []
    
    def _analyze_layout(self, page) -> Dict[str, Any]:
        """Analyze page layout for better extraction"""
        try:
            layout_info = {
                "page_width": page.width,
                "page_height": page.height,
                "text_blocks": [],
                "lines": []
            }
            
            # Extract text blocks
            text_blocks = page.extract_text_simple()
            if text_blocks:
                layout_info["text_blocks"] = text_blocks
            
            # Extract lines
            lines = page.lines
            if lines:
                layout_info["lines"] = [
                    {
                        "x0": line["x0"],
                        "y0": line["y0"],
                        "x1": line["x1"],
                        "y1": line["y1"],
                        "width": line["width"],
                        "height": line["height"]
                    }
                    for line in lines
                ]
            
            return layout_info
            
        except Exception as e:
            logger.error(f"Layout analysis failed: {e}")
            return {}
    
    def find_field_by_position(self, text: str, field_name: str, layout_info: Dict[str, Any]) -> Optional[str]:
        """Find field value based on position in layout"""
        try:
            # This is a simplified implementation
            # In practice, you'd use the layout_info to find fields by position
            
            if field_name == "cardholder_name":
                # Look for name patterns in the first part of the document
                lines = text.split('\n')[:10]  # First 10 lines
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['name', 'cardholder', 'account holder']):
                        # Extract name from the line
                        parts = line.split(':')
                        if len(parts) > 1:
                            return parts[1].strip()
            
            elif field_name == "total_amount_due":
                # Look for amount patterns
                lines = text.split('\n')
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['total', 'amount due', 'outstanding']):
                        # Extract amount from the line
                        import re
                        amount_match = re.search(r'[₹$]?\s*([\d,]+\.?\d*)', line)
                        if amount_match:
                            return amount_match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Position-based field extraction failed: {e}")
            return None

class SmartLayoutExtractor(LayoutExtractor):
    """Enhanced layout extractor with smart field detection"""
    
    def extract_fields_with_layout(self, pdf_path: str) -> Dict[str, Any]:
        """Extract fields using layout information"""
        try:
            # Get layout extraction result
            layout_result = self.extract_from_pdf(pdf_path)
            
            if not layout_result["extracted_text"]:
                return layout_result
            
            # Use layout information to improve field extraction
            fields = {}
            text = layout_result["extracted_text"]
            
            # Extract fields using layout-aware methods
            fields["cardholder_name"] = self._extract_name_with_layout(text, layout_result["layout_info"])
            fields["card_last_four"] = self._extract_card_number_with_layout(text, layout_result["layout_info"])
            fields["billing_period_start"], fields["billing_period_end"] = self._extract_billing_period_with_layout(text, layout_result["layout_info"])
            fields["payment_due_date"] = self._extract_due_date_with_layout(text, layout_result["layout_info"])
            fields["total_amount_due"] = self._extract_amount_with_layout(text, layout_result["layout_info"])
            
            return {
                "extracted_text": layout_result["extracted_text"],
                "extracted_fields": fields,
                "layout_info": layout_result["layout_info"],
                "extraction_method": "smart_layout",
                "extraction_steps": layout_result["extraction_steps"],
                "confidence_scores": self._calculate_layout_confidence(fields)
            }
            
        except Exception as e:
            logger.error(f"Smart layout extraction failed: {e}")
            return {
                "extracted_text": "",
                "extracted_fields": {},
                "layout_info": {},
                "extraction_method": "smart_layout_failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0}
            }
    
    def _extract_name_with_layout(self, text: str, layout_info: Dict[str, Any]) -> Optional[str]:
        """Extract cardholder name using layout information"""
        # Look in the header area (first few lines)
        lines = text.split('\n')[:15]
        for line in lines:
            if any(keyword in line.lower() for keyword in ['name', 'cardholder', 'account holder']):
                # Extract name after the keyword
                parts = line.split(':')
                if len(parts) > 1:
                    name = parts[1].strip()
                    if len(name) > 2:  # Reasonable name length
                        return name
        return None
    
    def _extract_card_number_with_layout(self, text: str, layout_info: Dict[str, Any]) -> Optional[str]:
        """Extract card number using layout information"""
        import re
        # Look for masked card numbers
        card_patterns = [
            r'\*{4,}\s*(\d{4})',
            r'(?:Card No|Card Number)[\s:]*\*{4,}\s*(\d{4})'
        ]
        
        for pattern in card_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_billing_period_with_layout(self, text: str, layout_info: Dict[str, Any]) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Extract billing period using layout information"""
        import re
        from datetime import datetime
        
        # Look for period patterns
        period_patterns = [
            r'(?:Statement Period|Billing Period)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
            r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s*to\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})'
        ]
        
        for pattern in period_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_date_str = match.group(1)
                end_date_str = match.group(2)
                start_date = self._parse_date(start_date_str)
                end_date = self._parse_date(end_date_str)
                return start_date, end_date
        
        return None, None
    
    def _extract_due_date_with_layout(self, text: str, layout_info: Dict[str, Any]) -> Optional[datetime]:
        """Extract payment due date using layout information"""
        import re
        from datetime import datetime
        
        due_date_patterns = [
            r'(?:Payment Due Date|Due Date)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
            r'(?:Due|Payment Due)[\s:]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})'
        ]
        
        for pattern in due_date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                return self._parse_date(date_str)
        return None
    
    def _extract_amount_with_layout(self, text: str, layout_info: Dict[str, Any]) -> Optional[float]:
        """Extract total amount using layout information"""
        import re
        
        amount_patterns = [
            r'(?:Total Amount Due|Amount Due|Outstanding)[\s:]*[₹$]?\s*([\d,]+\.?\d*)',
            r'(?:Total|Amount)[\s:]*[₹$]?\s*([\d,]+\.?\d*)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(",", "")
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        return None
    
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
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def _calculate_layout_confidence(self, fields: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for layout-based extraction"""
        confidence_scores = {}
        
        for field, value in fields.items():
            if value is not None:
                if field in ["cardholder_name", "card_last_four"]:
                    confidence_scores[field] = 0.85  # High confidence for layout-based text
                elif field in ["billing_period_start", "billing_period_end", "payment_due_date"]:
                    confidence_scores[field] = 0.80  # High confidence for layout-based dates
                elif field == "total_amount_due":
                    confidence_scores[field] = 0.90  # High confidence for layout-based amounts
                else:
                    confidence_scores[field] = 0.75  # Default confidence
            else:
                confidence_scores[field] = 0.0
        
        return confidence_scores
