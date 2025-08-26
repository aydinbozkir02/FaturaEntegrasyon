# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db
from models import (
    add_invoice, get_all_invoices, update_invoice, delete_invoice,
    get_contacts, get_contact, add_contact, update_contact, delete_contact
)
from utils import validate_invoice, generate_invoice_pdf

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/')
def home():
    return jsonify({"message": "Modüler Fatura API çalışıyor"}), 200

# ---- INVOICES ROUTES ----
@app.route('/invoices', methods=['GET'])
def get_invoices():
    return jsonify({"status": "success", "invoices": get_all_invoices()}), 200

@app.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    valid, msg = validate_invoice(data)
    if not valid:
        return jsonify({"status": "error", "message": msg}), 400
    invoice_id = add_invoice(data)
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

# ---- CONTACTS ROUTES ----
@app.route('/contacts', methods=['GET'])
def list_contacts():
    return jsonify({"status": "success", "contacts": get_contacts()}), 200

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact_by_id(contact_id):
    c = get_contact(contact_id)
    if not c:
        return jsonify({"status": "error", "message": "Müşteri bulunamadı"}), 404
    return jsonify({"status": "success", "contact": c}), 200

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.json or {}
    if not data.get("name"):
        return jsonify({"status": "error", "message": "name alanı zorunlu"}), 400
    new_id = add_contact(data)
    return jsonify({"status": "success", "contact_id": new_id}), 201

@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def edit_contact(contact_id):
    data = request.json or {}
    if not data.get("name"):
        return jsonify({"status": "error", "message": "name alanı zorunlu"}), 400
    ok = update_contact(contact_id, data)
    if not ok:
        return jsonify({"status": "error", "message": "Müşteri bulunamadı"}), 404
    return jsonify({"status": "success", "contact_id": contact_id}), 200

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def remove_contact(contact_id):
    ok = delete_contact(contact_id)
    if not ok:
        return jsonify({"status": "error", "message": "Müşteri bulunamadı"}), 404
    return jsonify({"status": "success", "message": f"Müşteri {contact_id} silindi"}), 200

if __name__ == '__main__':
    app.run(debug=True)
