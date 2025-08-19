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
    conn.commit()
    conn.close()

def get_db_connection():
    """Veritabanı bağlantısı oluştur ve döndür"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Satırları dict gibi kullanabilmek için
    return conn
