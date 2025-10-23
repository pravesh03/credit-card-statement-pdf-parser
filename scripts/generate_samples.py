"""
Generate synthetic credit card statement PDFs for testing
"""

import os
import sys
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class StatementGenerator:
    """Generate synthetic credit card statements"""
    
    def __init__(self, output_dir: str = "samples"):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def _setup_styles(self):
        """Setup custom styles"""
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='Amount',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_RIGHT,
            textColor=colors.red
        ))
    
    def generate_hdfc_statement(self):
        """Generate HDFC Bank statement"""
        filename = os.path.join(self.output_dir, "hdfc", "sample_statement.pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Header
        story.append(Paragraph("HDFC BANK LIMITED", self.styles['Header']))
        story.append(Paragraph("Credit Card Statement", self.styles['SubHeader']))
        story.append(Spacer(1, 12))
        
        # Cardholder info
        cardholder_name = "JOHN DOE"
        card_number = "**** **** **** 1234"
        story.append(Paragraph(f"<b>Name:</b> {cardholder_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Card No:</b> {card_number}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Billing period
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() - timedelta(days=1)
        due_date = datetime.now() + timedelta(days=15)
        
        story.append(Paragraph(f"<b>Statement Period:</b> {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Payment Due Date:</b> {due_date.strftime('%d/%m/%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Transaction table
        transactions = [
            ["Date", "Description", "Amount"],
            ["15/11/2023", "AMAZON PAY", "₹2,500.00"],
            ["18/11/2023", "SWIGGY", "₹450.00"],
            ["22/11/2023", "PETROL PUMP", "₹1,200.00"],
            ["25/11/2023", "NETFLIX", "₹199.00"],
            ["28/11/2023", "GROCERY STORE", "₹3,200.00"]
        ]
        
        table = Table(transactions)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total amount due
        total_amount = 7549.00
        story.append(Paragraph(f"<b>Total Amount Due:</b> ₹{total_amount:,.2f}", self.styles['Amount']))
        
        doc.build(story)
        return filename
    
    def generate_sbi_statement(self):
        """Generate SBI statement"""
        filename = os.path.join(self.output_dir, "sbi", "sample_statement.pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Header
        story.append(Paragraph("STATE BANK OF INDIA", self.styles['Header']))
        story.append(Paragraph("Credit Card Statement", self.styles['SubHeader']))
        story.append(Spacer(1, 12))
        
        # Cardholder info
        cardholder_name = "JANE SMITH"
        card_number = "**** **** **** 5678"
        story.append(Paragraph(f"<b>Cardholder Name:</b> {cardholder_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Card Number:</b> {card_number}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Billing period
        start_date = datetime.now() - timedelta(days=28)
        end_date = datetime.now() - timedelta(days=2)
        due_date = datetime.now() + timedelta(days=12)
        
        story.append(Paragraph(f"<b>Billing Period:</b> {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Due Date:</b> {due_date.strftime('%d-%m-%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Transaction table
        transactions = [
            ["Date", "Merchant", "Amount"],
            ["10/11/2023", "UBER", "₹350.00"],
            ["12/11/2023", "ZOMATO", "₹680.00"],
            ["15/11/2023", "BOOKMYSHOW", "₹450.00"],
            ["20/11/2023", "FLIPKART", "₹1,850.00"],
            ["25/11/2023", "MEDICAL STORE", "₹320.00"]
        ]
        
        table = Table(transactions)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total amount due
        total_amount = 3450.00
        story.append(Paragraph(f"<b>Amount Due:</b> ₹{total_amount:,.2f}", self.styles['Amount']))
        
        doc.build(story)
        return filename
    
    def generate_icici_statement(self):
        """Generate ICICI statement"""
        filename = os.path.join(self.output_dir, "icici", "sample_statement.pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Header
        story.append(Paragraph("ICICI BANK LIMITED", self.styles['Header']))
        story.append(Paragraph("Credit Card Statement", self.styles['SubHeader']))
        story.append(Spacer(1, 12))
        
        # Cardholder info
        cardholder_name = "ALICE JOHNSON"
        card_number = "**** **** **** 9012"
        story.append(Paragraph(f"<b>Account Holder:</b> {cardholder_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Card No:</b> {card_number}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Billing period
        start_date = datetime.now() - timedelta(days=25)
        end_date = datetime.now() - timedelta(days=3)
        due_date = datetime.now() + timedelta(days=18)
        
        story.append(Paragraph(f"<b>Statement Period:</b> {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Payment Due Date:</b> {due_date.strftime('%d.%m.%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Transaction table
        transactions = [
            ["Date", "Description", "Amount"],
            ["08/11/2023", "SPOTIFY", "₹99.00"],
            ["14/11/2023", "AMAZON PRIME", "₹149.00"],
            ["18/11/2023", "RESTAURANT", "₹1,200.00"],
            ["22/11/2023", "ONLINE SHOPPING", "₹2,800.00"],
            ["26/11/2023", "CAB RIDE", "₹180.00"]
        ]
        
        table = Table(transactions)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total amount due
        total_amount = 4428.00
        story.append(Paragraph(f"<b>Total Amount Due:</b> ₹{total_amount:,.2f}", self.styles['Amount']))
        
        doc.build(story)
        return filename
    
    def generate_axis_statement(self):
        """Generate Axis Bank statement"""
        filename = os.path.join(self.output_dir, "axis", "sample_statement.pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Header
        story.append(Paragraph("AXIS BANK LIMITED", self.styles['Header']))
        story.append(Paragraph("Credit Card Statement", self.styles['SubHeader']))
        story.append(Spacer(1, 12))
        
        # Cardholder info
        cardholder_name = "BOB WILSON"
        card_number = "**** **** **** 3456"
        story.append(Paragraph(f"<b>Name:</b> {cardholder_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Card Number:</b> {card_number}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Billing period
        start_date = datetime.now() - timedelta(days=32)
        end_date = datetime.now() - timedelta(days=4)
        due_date = datetime.now() + timedelta(days=20)
        
        story.append(Paragraph(f"<b>Billing Period:</b> {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Due Date:</b> {due_date.strftime('%d/%m/%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Transaction table
        transactions = [
            ["Date", "Merchant", "Amount"],
            ["05/11/2023", "APPLE STORE", "₹1,200.00"],
            ["09/11/2023", "GOOGLE PLAY", "₹299.00"],
            ["16/11/2023", "HOTEL BOOKING", "₹3,500.00"],
            ["21/11/2023", "FUEL STATION", "₹1,800.00"],
            ["28/11/2023", "ONLINE RETAIL", "₹950.00"]
        ]
        
        table = Table(transactions)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total amount due
        total_amount = 7749.00
        story.append(Paragraph(f"<b>Outstanding:</b> ₹{total_amount:,.2f}", self.styles['Amount']))
        
        doc.build(story)
        return filename
    
    def generate_citibank_statement(self):
        """Generate Citibank statement"""
        filename = os.path.join(self.output_dir, "citibank", "sample_statement.pdf")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Header
        story.append(Paragraph("CITIBANK N.A.", self.styles['Header']))
        story.append(Paragraph("Credit Card Statement", self.styles['SubHeader']))
        story.append(Spacer(1, 12))
        
        # Cardholder info
        cardholder_name = "CAROL DAVIS"
        card_number = "**** **** **** 7890"
        story.append(Paragraph(f"<b>Cardholder Name:</b> {cardholder_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Card No:</b> {card_number}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Billing period
        start_date = datetime.now() - timedelta(days=29)
        end_date = datetime.now() - timedelta(days=1)
        due_date = datetime.now() + timedelta(days=14)
        
        story.append(Paragraph(f"<b>Statement Period:</b> {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Payment Due Date:</b> {due_date.strftime('%m/%d/%Y')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Transaction table
        transactions = [
            ["Date", "Description", "Amount"],
            ["12/11/2023", "STARBUCKS", "₹450.00"],
            ["15/11/2023", "MOVIE TICKETS", "₹600.00"],
            ["19/11/2023", "ONLINE SHOPPING", "₹2,200.00"],
            ["24/11/2023", "GYM MEMBERSHIP", "₹1,500.00"],
            ["28/11/2023", "PHARMACY", "₹380.00"]
        ]
        
        table = Table(transactions)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.mistyrose),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Total amount due
        total_amount = 5130.00
        story.append(Paragraph(f"<b>Total Amount Due:</b> ₹{total_amount:,.2f}", self.styles['Amount']))
        
        doc.build(story)
        return filename
    
    def generate_all_samples(self):
        """Generate all sample statements"""
        print("Generating sample credit card statements...")
        
        files = []
        files.append(self.generate_hdfc_statement())
        files.append(self.generate_sbi_statement())
        files.append(self.generate_icici_statement())
        files.append(self.generate_axis_statement())
        files.append(self.generate_citibank_statement())
        
        print(f"Generated {len(files)} sample statements:")
        for file in files:
            print(f"  - {file}")
        
        return files

if __name__ == "__main__":
    generator = StatementGenerator()
    generator.generate_all_samples()
