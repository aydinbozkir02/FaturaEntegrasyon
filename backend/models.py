from db import get_db_connection
import json

# ---- INVOICES CRUD ----
def get_all_invoices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
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
    """, (data['contact_id'], data['issue_date'], data['due_date'],
          data['status'], json.dumps(data['lines'])))
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
    """, (data['contact_id'], data['issue_date'], data['due_date'],
          data['status'], json.dumps(data['lines']), invoice_id))
    conn.commit()
    conn.close()
    return True

def delete_invoice(invoice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invoices WHERE invoice_id=?", (invoice_id,))
    conn.commit()
    conn.close()


# ---- CONTACTS CRUD ----
def get_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY contact_id DESC")
    rows = cur.fetchall()
    contacts = []
    for r in rows:
        contacts.append(dict(r))
    conn.close()
    return contacts

def get_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE contact_id=?", (contact_id,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None

def add_contact(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contacts (name, tax_no, email, phone, address, city, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name"), data.get("tax_no"), data.get("email"),
        data.get("phone"), data.get("address"), data.get("city"),
        data.get("country")
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def update_contact(contact_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM contacts WHERE contact_id=?", (contact_id,))
    if cur.fetchone() is None:
        conn.close()
        return False
    cur.execute("""
        UPDATE contacts
        SET name=?, tax_no=?, email=?, phone=?, address=?, city=?, country=?
        WHERE contact_id=?
    """, (
        data.get("name"), data.get("tax_no"), data.get("email"),
        data.get("phone"), data.get("address"), data.get("city"),
        data.get("country"), contact_id
    ))
    conn.commit()
    conn.close()
    return True

def delete_contact(contact_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE contact_id=?", (contact_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted

# ---- ITEMS CRUD ----
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items ORDER BY item_id DESC")
    rows = cur.fetchall()
    items = [dict(r) for r in rows]
    conn.close()
    return items

def get_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_id=?", (item_id,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None

def add_item(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO items (sku, name, unit, unit_price, tax_rate, stock_qty)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("sku"), data.get("name"), data.get("unit"),
        data.get("unit_price"), data.get("tax_rate"),
        data.get("stock_qty", 0)
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def update_item(item_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM items WHERE item_id=?", (item_id,))
    if cur.fetchone() is None:
        conn.close()
        return False
    cur.execute("""
        UPDATE items
        SET sku=?, name=?, unit=?, unit_price=?, tax_rate=?, stock_qty=?
        WHERE item_id=?
    """, (
        data.get("sku"), data.get("name"), data.get("unit"),
        data.get("unit_price"), data.get("tax_rate"),
        data.get("stock_qty", 0), item_id
    ))
    conn.commit()
    conn.close()
    return True

def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE item_id=?", (item_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted
