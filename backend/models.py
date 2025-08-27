from db import get_db_connection
import json
from datetime import datetime

# ---- INVOICES CRUD ----
def get_all_invoices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    invoices = []
    for row in rows:
        # lines alanı JSON tutuluyor; güvenli parse
        raw_lines = row["lines"]
        try:
            lines = json.loads(raw_lines) if raw_lines else []
        except Exception:
            lines = []
        invoices.append({
            "invoice_id": row["invoice_id"],
            "contact_id": row["contact_id"],
            "issue_date": row["issue_date"],
            "due_date": row["due_date"],
            "status": row["status"],
            "lines": lines
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
          data['status'], json.dumps(data.get('lines', []))))
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
          data['status'], json.dumps(data.get('lines', [])), invoice_id))
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


# ---- STOCK MOVEMENTS (SQLite) -----------------------------------------------
# Not: Bu bölüm SQLAlchemy DEĞİL; sqlite3 ile çalışır ve items.stock_qty'yi günceller.

def get_stock_movements(item_id=None, limit=200):
    """
    Stok hareketlerini son eklenenden başlayarak getirir.
    item_id verilirse yalnızca o ürüne ait hareketleri döndürür.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    if item_id:
        cur.execute("""
            SELECT * FROM stock_movements
            WHERE item_id=?
            ORDER BY movement_id DESC
            LIMIT ?
        """, (item_id, limit))
    else:
        cur.execute("""
            SELECT * FROM stock_movements
            ORDER BY movement_id DESC
            LIMIT ?
        """, (limit,))
    rows = cur.fetchall()
    data = [dict(r) for r in rows]
    conn.close()
    return data

def add_stock_movement(item_id, change, reason='manual', ref_table=None, ref_id=None):
    """
    Stok değişikliği uygular ve log yazar.
    change: +giriş / -çıkış
    DÖNÜŞ: {"movement": {...}, "item": {"item_id":..., "stock_qty":...}}
    """
    # tip/limit kontrolleri
    try:
        item_id = int(item_id)
        change = int(change)
    except (TypeError, ValueError):
        return None

    if item_id <= 0 or change == 0:
        return None

    conn = get_db_connection()
    cur = conn.cursor()

    # ürün var mı?
    cur.execute("SELECT item_id, stock_qty FROM items WHERE item_id=?", (item_id,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return None

    current_qty = int(r["stock_qty"] or 0)
    new_qty = current_qty + change
    if new_qty < 0:
        new_qty = 0  # negatif stok olmasın

    # ürün güncelle
    cur.execute("UPDATE items SET stock_qty=? WHERE item_id=?", (new_qty, item_id))

    # hareket ekle
    created_at = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO stock_movements (item_id, change, reason, ref_table, ref_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item_id, change, reason, ref_table, ref_id, created_at))

    conn.commit()
    movement_id = cur.lastrowid
    conn.close()

    return {
        "movement": {
            "movement_id": movement_id,
            "item_id": item_id,
            "change": change,
            "reason": reason,
            "ref_table": ref_table,
            "ref_id": ref_id,
            "created_at": created_at
        },
        "item": {"item_id": item_id, "stock_qty": new_qty}
    }
