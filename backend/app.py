from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock veri tabanı
invoices = []

@app.route("/create_invoice", methods=["POST"])
def create_invoice():
    data = request.json
    invoice_id = len(invoices) + 1
    invoice = {
        "invoice_id": invoice_id,
        "contact_id": data.get("contact_id", 1),
        "issue_date": data.get("issue_date", "2025-08-13"),
        "due_date": data.get("due_date", "2025-08-20"),
        "lines": data.get("lines", [{"item_id": 1, "quantity": 1, "unit_price": 100}]),
        "status": "draft"
    }
    invoices.append(invoice)
    return jsonify({"status": "success", "invoice": invoice}), 201

@app.route("/invoices", methods=["GET"])
def get_invoices():
    return jsonify({"status": "success", "invoices": invoices}), 200

@app.route("/delete_invoice/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    global invoices
    invoices = [inv for inv in invoices if inv["invoice_id"] != invoice_id]
    return jsonify({"status": "success", "message": f"Invoice {invoice_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
