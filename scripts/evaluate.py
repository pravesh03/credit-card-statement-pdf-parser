"""
Evaluation script for credit card statement parsing
"""

import os
import sys
import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.extractor import StatementExtractor
from backend.app.ai.ai_provider import get_ai_provider

class StatementEvaluator:
    """Evaluate statement parsing performance"""
    
    def __init__(self, samples_dir: str = "samples"):
        self.samples_dir = Path(samples_dir)
        self.extractor = StatementExtractor()
        self.results = []
        
        # Expected values for each sample (would be manually verified)
        self.expected_values = {
            "hdfc/sample_statement.pdf": {
                "cardholder_name": "JOHN DOE",
                "card_last_four": "1234",
                "total_amount_due": 7549.0,
                "payment_due_date": "2023-12-15",
                "billing_period_start": "2023-11-01",
                "billing_period_end": "2023-11-30"
            },
            "sbi/sample_statement.pdf": {
                "cardholder_name": "JANE SMITH",
                "card_last_four": "5678",
                "total_amount_due": 3450.0,
                "payment_due_date": "2023-12-12",
                "billing_period_start": "2023-11-01",
                "billing_period_end": "2023-11-30"
            },
            "icici/sample_statement.pdf": {
                "cardholder_name": "ALICE JOHNSON",
                "card_last_four": "9012",
                "total_amount_due": 4428.0,
                "payment_due_date": "2023-12-18",
                "billing_period_start": "2023-11-01",
                "billing_period_end": "2023-11-30"
            },
            "axis/sample_statement.pdf": {
                "cardholder_name": "BOB WILSON",
                "card_last_four": "3456",
                "total_amount_due": 7749.0,
                "payment_due_date": "2023-12-20",
                "billing_period_start": "2023-11-01",
                "billing_period_end": "2023-11-30"
            },
            "citibank/sample_statement.pdf": {
                "cardholder_name": "CAROL DAVIS",
                "card_last_four": "7890",
                "total_amount_due": 5130.0,
                "payment_due_date": "2023-12-14",
                "billing_period_start": "2023-11-01",
                "billing_period_end": "2023-11-30"
            }
        }
    
    def evaluate_sample(self, pdf_path: Path, issuer: str = None) -> Dict[str, Any]:
        """Evaluate a single sample PDF"""
        print(f"Evaluating {pdf_path}...")
        
        try:
            # Extract fields
            result = self.extractor.extract_from_pdf(str(pdf_path), issuer)
            
            # Get expected values
            relative_path = str(pdf_path.relative_to(self.samples_dir))
            expected = self.expected_values.get(relative_path, {})
            
            # Calculate accuracy for each field
            field_accuracy = {}
            for field in ["cardholder_name", "card_last_four", "total_amount_due", 
                          "payment_due_date", "billing_period_start", "billing_period_end"]:
                extracted_value = result["extracted_fields"].get(field)
                expected_value = expected.get(field)
                
                if expected_value is None:
                    field_accuracy[field] = None  # No expected value
                elif extracted_value is None:
                    field_accuracy[field] = 0.0  # Missing extraction
                else:
                    # Calculate accuracy based on field type
                    if field in ["cardholder_name", "card_last_four"]:
                        # String comparison
                        field_accuracy[field] = 1.0 if str(extracted_value).upper() == str(expected_value).upper() else 0.0
                    elif field == "total_amount_due":
                        # Numeric comparison with tolerance
                        tolerance = 0.01
                        field_accuracy[field] = 1.0 if abs(float(extracted_value) - float(expected_value)) <= tolerance else 0.0
                    else:
                        # Date comparison
                        try:
                            if isinstance(extracted_value, str):
                                extracted_date = datetime.strptime(extracted_value, "%Y-%m-%d").date()
                            else:
                                extracted_date = extracted_value.date()
                            
                            if isinstance(expected_value, str):
                                expected_date = datetime.strptime(expected_value, "%Y-%m-%d").date()
                            else:
                                expected_date = expected_value.date()
                            
                            field_accuracy[field] = 1.0 if extracted_date == expected_date else 0.0
                        except:
                            field_accuracy[field] = 0.0
            
            # Calculate overall accuracy
            valid_fields = [acc for acc in field_accuracy.values() if acc is not None]
            overall_accuracy = sum(valid_fields) / len(valid_fields) if valid_fields else 0.0
            
            evaluation_result = {
                "filename": pdf_path.name,
                "issuer": issuer or "unknown",
                "extraction_method": result["extraction_method"],
                "overall_confidence": result["overall_confidence"],
                "field_accuracy": field_accuracy,
                "overall_accuracy": overall_accuracy,
                "extracted_fields": result["extracted_fields"],
                "expected_fields": expected,
                "extraction_steps": result["extraction_steps"],
                "llm_rationale": result.get("llm_rationale", ""),
                "timestamp": datetime.now().isoformat()
            }
            
            return evaluation_result
            
        except Exception as e:
            print(f"Error evaluating {pdf_path}: {e}")
            return {
                "filename": pdf_path.name,
                "issuer": issuer or "unknown",
                "error": str(e),
                "overall_accuracy": 0.0,
                "overall_confidence": 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    def evaluate_all_samples(self) -> List[Dict[str, Any]]:
        """Evaluate all sample PDFs"""
        print("Starting evaluation of all samples...")
        
        results = []
        
        # Find all PDF files in samples directory
        for pdf_file in self.samples_dir.rglob("*.pdf"):
            # Determine issuer from directory name
            issuer = pdf_file.parent.name if pdf_file.parent.name != "samples" else None
            
            result = self.evaluate_sample(pdf_file, issuer)
            results.append(result)
        
        self.results = results
        return results
    
    def generate_report(self, output_file: str = "evaluation_report.csv") -> str:
        """Generate evaluation report"""
        if not self.results:
            self.evaluate_all_samples()
        
        # Calculate summary statistics
        total_samples = len(self.results)
        successful_extractions = len([r for r in self.results if "error" not in r])
        avg_accuracy = sum(r["overall_accuracy"] for r in self.results if "error" not in r) / max(successful_extractions, 1)
        avg_confidence = sum(r["overall_confidence"] for r in self.results if "error" not in r) / max(successful_extractions, 1)
        
        # Field-level accuracy
        field_accuracy = {}
        for field in ["cardholder_name", "card_last_four", "total_amount_due", 
                      "payment_due_date", "billing_period_start", "billing_period_end"]:
            field_results = [r["field_accuracy"].get(field) for r in self.results 
                           if "error" not in r and r["field_accuracy"].get(field) is not None]
            field_accuracy[field] = sum(field_results) / len(field_results) if field_results else 0.0
        
        # Write CSV report
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow([
                "Filename", "Issuer", "Extraction Method", "Overall Accuracy", 
                "Overall Confidence", "Cardholder Name Acc", "Card Last 4 Acc",
                "Total Amount Acc", "Due Date Acc", "Period Start Acc", "Period End Acc",
                "Error Message", "LLM Rationale"
            ])
            
            # Data rows
            for result in self.results:
                writer.writerow([
                    result["filename"],
                    result["issuer"],
                    result.get("extraction_method", ""),
                    f"{result['overall_accuracy']:.3f}",
                    f"{result['overall_confidence']:.3f}",
                    f"{result['field_accuracy'].get('cardholder_name', 0):.3f}",
                    f"{result['field_accuracy'].get('card_last_four', 0):.3f}",
                    f"{result['field_accuracy'].get('total_amount_due', 0):.3f}",
                    f"{result['field_accuracy'].get('payment_due_date', 0):.3f}",
                    f"{result['field_accuracy'].get('billing_period_start', 0):.3f}",
                    f"{result['field_accuracy'].get('billing_period_end', 0):.3f}",
                    result.get("error", ""),
                    result.get("llm_rationale", "")
                ])
        
        # Generate summary report
        summary = {
            "evaluation_timestamp": datetime.now().isoformat(),
            "total_samples": total_samples,
            "successful_extractions": successful_extractions,
            "failed_extractions": total_samples - successful_extractions,
            "average_accuracy": avg_accuracy,
            "average_confidence": avg_confidence,
            "field_accuracy": field_accuracy,
            "ai_provider": "mock"  # Would be dynamic in real implementation
        }
        
        with open("evaluation_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nEvaluation Report Generated:")
        print(f"  CSV Report: {output_file}")
        print(f"  Summary: evaluation_summary.json")
        print(f"\nSummary Statistics:")
        print(f"  Total Samples: {total_samples}")
        print(f"  Successful: {successful_extractions}")
        print(f"  Failed: {total_samples - successful_extractions}")
        print(f"  Average Accuracy: {avg_accuracy:.3f}")
        print(f"  Average Confidence: {avg_confidence:.3f}")
        print(f"\nField Accuracy:")
        for field, accuracy in field_accuracy.items():
            print(f"  {field}: {accuracy:.3f}")
        
        return output_file

def main():
    """Main evaluation function"""
    evaluator = StatementEvaluator()
    
    print("Credit Card Statement Parser - Evaluation")
    print("=" * 50)
    
    # Run evaluation
    results = evaluator.evaluate_all_samples()
    
    # Generate report
    report_file = evaluator.generate_report()
    
    print(f"\nEvaluation completed! Check {report_file} for detailed results.")

if __name__ == "__main__":
    main()
