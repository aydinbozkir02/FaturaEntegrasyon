from db import get_db_connection
import json

# Fatura ekleme
def add_invoice(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO invoice (contact_id, issue_date, due_date, status)
        VALUES (?, ?, ?, ?)
    ''', (data["contact_id"], data["issue_date"], data["due_date"], data["status"]))
    invoice_id = cursor.lastrowid

    for line in data["lines"]:
        cursor.execute('''
            INSERT INTO invoice_line (invoice_id, item_description, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        ''', (invoice_id, line["description"], line["quantity"], line["unit_price"]))

    conn.commit()
    conn.close()
    return invoice_id

# Tüm faturaları çek
# Doğru tablo adı kullan
def get_all_invoices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")  # <--- invoices olmalı, invoice değil
    rows = cursor.fetchall()
    invoices = []
    for row in rows:
        invoices.append({
            "invoice_id": row["invoice_id"],
            "contact_id": row["contact_id"],
            "issue_date": row["issue_date"],
            "due_date": row["due_date"],
            "status": row["status"],
            "lines": json.loads(row["lines"])
        })
    conn.close()
    return invoices

def add_invoice(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO invoices (contact_id, issue_date, due_date, status, lines)
        VALUES (?, ?, ?, ?, ?)
    """, (data['contact_id'], data['issue_date'], data['due_date'], data['status'], json.dumps(data['lines'])))
    conn.commit()
    invoice_id = cursor.lastrowid
    conn.close()
    return invoice_id

def update_invoice(invoice_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices WHERE invoice_id=?", (invoice_id,))
    if cursor.fetchone() is None:
        conn.close()
        return False
    cursor.execute("""
        UPDATE invoices
        SET contact_id=?, issue_date=?, due_date=?, status=?, lines=?
        WHERE invoice_id=?
    """, (data['contact_id'], data['issue_date'], data['due_date'], data['status'], json.dumps(data['lines']), invoice_id))
    conn.commit()
    conn.close()
    return True

def delete_invoice(invoice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invoices WHERE invoice_id=?", (invoice_id,))
    conn.commit()
    conn.close()
