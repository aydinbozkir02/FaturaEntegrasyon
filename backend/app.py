from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "invoices.json"

# JSON dosyası yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Verileri oku
def read_invoices():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Verileri yaz
def write_invoices(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return jsonify({"message": "Mock Invoice API is running"}), 200

# Tüm faturaları listele
@app.route("/invoices", methods=["GET"])
def get_invoices():
    invoices = read_invoices()
    return jsonify({"status": "success", "invoices": invoices}), 200

# Yeni fatura oluştur
@app.route("/invoices", methods=["POST"])
def create_invoice():
    data = request.json

    # Zorunlu alan kontrolü
    required_fields = ["contact_id", "due_date", "issue_date", "lines", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"{field} is required"}), 400

    # Otomatik invoice_id atama
    invoices = read_invoices()
    data["invoice_id"] = len(invoices) + 1
    invoices.append(data)
    write_invoices(invoices)

    return jsonify({"status": "success", "invoice": data}), 201

if __name__ == "__main__":
    app.run(debug=True)
