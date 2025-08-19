# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection, init_db
from models import add_invoice, get_all_invoices, update_invoice, delete_invoice
from utils import validate_invoice, generate_invoice_pdf

app = Flask(__name__)
CORS(app)  # Tüm domainlere izin verir

# Veritabanı setup
init_db()

@app.route('/')
def home():
    return jsonify({"message": "Modüler Fatura API çalışıyor"}), 200

@app.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = get_all_invoices()
    return jsonify({"status": "success", "invoices": invoices}), 200

@app.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    print("POST alındı:", data)  # Log terminale düşecek
    valid, msg = validate_invoice(data)
    if not valid:
        return jsonify({"status": "error", "message": msg}), 400

    invoice_id = add_invoice(data)
    print(f"Fatura kaydedildi. ID: {invoice_id}")  # Log kaydı
    return jsonify({"status": "success", "invoice_id": invoice_id}), 201

@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def edit_invoice(invoice_id):
    data = request.json
    updated = update_invoice(invoice_id, data)
    if not updated:
        return jsonify({"status": "error", "message": "Fatura bulunamadı"}), 404
    return jsonify({"status": "success", "invoice_id": invoice_id}), 200

@app.route('/invoices/<int:invoice_id>/pdf', methods=['GET'])
def download_invoice(invoice_id):
    invoices = get_all_invoices()
    invoice = next((inv for inv in invoices if inv['invoice_id'] == invoice_id), None)
    if not invoice:
        return jsonify({"status": "error", "message": "Fatura bulunamadı"}), 404

    pdf_path = generate_invoice_pdf(invoice)
    return jsonify({"status": "success", "pdf_path": pdf_path}), 200

@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def remove_invoice(invoice_id):
    delete_invoice(invoice_id)
    return jsonify({"status": "success", "message": f"Fatura {invoice_id} silindi"}), 200

if __name__ == '__main__':
    app.run(debug=True)
