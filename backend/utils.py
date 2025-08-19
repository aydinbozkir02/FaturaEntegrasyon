
from fpdf import FPDF

def validate_invoice(data):
    required_fields = ["contact_id", "issue_date", "due_date", "status", "lines"]
    for field in required_fields:
        if field not in data:
            return False, f"{field} alanı gerekli"
    if not isinstance(data['lines'], list) or len(data['lines']) == 0:
        return False, "lines alanı boş olamaz ve liste olmalı"
    return True, "Geçerli"

def generate_invoice_pdf(invoice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Fatura ID: {invoice['invoice_id']}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Tarih: {invoice['issue_date']}", ln=True)
    pdf.cell(0, 10, f"Vade: {invoice['due_date']}", ln=True)
    pdf.cell(0, 10, f"Durum: {invoice['status']}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "Ürünler:", ln=True)
    for line in invoice['lines']:
        pdf.cell(0, 10, f"{line['description']} - {line['quantity']} x {line['unit_price']}", ln=True)
    pdf_path = f"invoice_{invoice['invoice_id']}.pdf"
    pdf.output(pdf_path)
    return pdf_path
