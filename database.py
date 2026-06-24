import sqlite3
import datetime
from config import DB_NAME

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized")

def save_price_to_db(product_name: str, price: float):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (product_name, price) VALUES (?, ?)",
            (product_name, price)
        )
        conn.commit()
        conn.close()
        print(f"Saved: {product_name} - {price} ₽ ({datetime.datetime.now()})")
    except Exception as e:
        print(f"Error saving to database: {e}")