"""
OCR extraction using Tesseract
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from typing import Dict, Any, Optional, List
import logging
import io

logger = logging.getLogger(__name__)

class OCRExtractor:
    """OCR-based text extraction using Tesseract"""
    
    def __init__(self, language: str = "eng", confidence_threshold: float = 0.6):
        self.language = language
        self.confidence_threshold = confidence_threshold
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text from PDF using OCR"""
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(pdf_path)
            all_text = ""
            extraction_steps = {}
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Try to get text directly first
                text = page.get_text()
                if text.strip():
                    all_text += text + "\n"
                    extraction_steps[f"page_{page_num}"] = "Direct text extraction"
                    continue
                
                # If no text, use OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scaling for better OCR
                img_data = pix.tobytes("png")
                
                # Preprocess image for better OCR
                processed_img = self._preprocess_image(img_data)
                
                # Extract text with confidence
                ocr_data = pytesseract.image_to_data(
                    processed_img, 
                    lang=self.language, 
                    output_type=pytesseract.Output.DICT
                )
                
                # Filter by confidence
                confident_text = []
                for i, conf in enumerate(ocr_data['conf']):
                    if int(conf) > self.confidence_threshold * 100:
                        text = ocr_data['text'][i].strip()
                        if text:
                            confident_text.append(text)
                
                page_text = " ".join(confident_text)
                all_text += page_text + "\n"
                extraction_steps[f"page_{page_num}"] = f"OCR extraction (confidence > {self.confidence_threshold})"
            
            doc.close()
            
            return {
                "extracted_text": all_text.strip(),
                "extraction_method": "ocr_tesseract",
                "extraction_steps": extraction_steps,
                "confidence_scores": {"overall": 0.7}  # OCR confidence
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {
                "extracted_text": "",
                "extraction_method": "ocr_failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0}
            }
    
    def _preprocess_image(self, img_data: bytes) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert bytes to PIL Image
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Apply preprocessing
            # 1. Resize if too small
            height, width = img_array.shape
            if height < 100 or width < 100:
                scale_factor = max(100/height, 100/width)
                new_height = int(height * scale_factor)
                new_width = int(width * scale_factor)
                img_array = cv2.resize(img_array, (new_width, new_height))
            
            # 2. Denoise
            img_array = cv2.medianBlur(img_array, 3)
            
            # 3. Enhance contrast
            img_array = cv2.convertScaleAbs(img_array, alpha=1.2, beta=10)
            
            # 4. Apply threshold
            _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Convert back to PIL Image
            return Image.fromarray(img_array)
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            # Return original image if preprocessing fails
            return Image.open(io.BytesIO(img_data))
    
    def extract_text_with_confidence(self, img_data: bytes) -> Dict[str, Any]:
        """Extract text with confidence scores"""
        try:
            processed_img = self._preprocess_image(img_data)
            
            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(
                processed_img,
                lang=self.language,
                output_type=pytesseract.Output.DICT
            )
            
            # Process results
            words = []
            confidences = []
            
            for i, conf in enumerate(ocr_data['conf']):
                text = ocr_data['text'][i].strip()
                if text and int(conf) > 0:
                    words.append(text)
                    confidences.append(int(conf) / 100.0)
            
            # Calculate overall confidence
            overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "text": " ".join(words),
                "words": words,
                "confidences": confidences,
                "overall_confidence": overall_confidence,
                "word_count": len(words)
            }
            
        except Exception as e:
            logger.error(f"OCR with confidence failed: {e}")
            return {
                "text": "",
                "words": [],
                "confidences": [],
                "overall_confidence": 0.0,
                "word_count": 0
            }

class HybridExtractor:
    """Hybrid extractor that combines direct text extraction and OCR"""
    
    def __init__(self, language: str = "eng", confidence_threshold: float = 0.6):
        self.ocr_extractor = OCRExtractor(language, confidence_threshold)
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text using hybrid approach"""
        try:
            doc = fitz.open(pdf_path)
            all_text = ""
            extraction_steps = {}
            has_direct_text = False
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Try direct text extraction first
                direct_text = page.get_text()
                if direct_text.strip():
                    all_text += direct_text + "\n"
                    has_direct_text = True
                    extraction_steps[f"page_{page_num}"] = "Direct text extraction"
                    continue
                
                # Fall back to OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                
                ocr_result = self.ocr_extractor.extract_text_with_confidence(img_data)
                if ocr_result["text"]:
                    all_text += ocr_result["text"] + "\n"
                    extraction_steps[f"page_{page_num}"] = f"OCR extraction (confidence: {ocr_result['overall_confidence']:.2f})"
            
            doc.close()
            
            return {
                "extracted_text": all_text.strip(),
                "extraction_method": "hybrid_direct_ocr" if has_direct_text else "hybrid_ocr_only",
                "extraction_steps": extraction_steps,
                "confidence_scores": {"overall": 0.9 if has_direct_text else 0.7}
            }
            
        except Exception as e:
            logger.error(f"Hybrid extraction failed: {e}")
            return {
                "extracted_text": "",
                "extraction_method": "hybrid_failed",
                "extraction_steps": {"error": str(e)},
                "confidence_scores": {"overall": 0.0}
            }
