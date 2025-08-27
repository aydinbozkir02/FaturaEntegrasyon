# db.py
import sqlite3

DB_NAME = "invoices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            lines TEXT NOT NULL
        )
    """)
    # Yeni: contacts tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tax_no TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT
        )
    """)

    # Yeni: items tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            name TEXT NOT NULL,
            unit TEXT,
            unit_price REAL NOT NULL,
            tax_rate REAL NOT NULL,
            stock_qty INTEGER DEFAULT 0
        )
    """)

    # EK: stock_movements tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_movements (
            movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id     INTEGER NOT NULL,
            change      INTEGER NOT NULL,         -- +giriş / -çıkış
            reason      TEXT,                     -- 'manual', 'invoice' vb.
            ref_table   TEXT,                     -- örn. 'invoices'
            ref_id      INTEGER,                  -- ilgili kayıt id
            created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            FOREIGN KEY (item_id) REFERENCES items(item_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()

def get_db_connection():
    import sqlite3
    conn = sqlite3.connect('invoices.db')
    conn.row_factory = sqlite3.Row
    # EK: foreign key desteği
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
