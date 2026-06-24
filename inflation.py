from typing import Optional
import sqlite3
from config import DB_NAME, PRODUCT_NAME

def calculate_inflation(days: int = 30) -> Optional[float]:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT price FROM prices
            WHERE product_name = ?
            AND timestamp >= datetime('now', ?)
            ORDER BY timestamp ASC
            LIMIT 1
        """, (PRODUCT_NAME, f'-{days} days'))
        old_price_row = cursor.fetchone()
        
        cursor.execute("""
            SELECT price FROM prices
            WHERE product_name = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (PRODUCT_NAME,))
        new_price_row = cursor.fetchone()
        
        conn.close()
        
        if old_price_row and new_price_row and old_price_row[0] > 0:
            old_price = old_price_row[0]
            new_price = new_price_row[0]
            inflation_percent = ((new_price - old_price) / old_price) * 100
            return round(inflation_percent, 2)
        
        return None
    except Exception as e:
        print(f"Error calculating inflation: {e}")
        return None

def print_inflation_report():
    print(f"\n📊 --- Inflation for '{PRODUCT_NAME}' ---")
    periods = {'week': 7, 'month': 30, 'quarter': 90, 'year': 365}
    for period_name, days in periods.items():
        inf = calculate_inflation(days)
        if inf is not None:
            sign = "+" if inf > 0 else ""
            print(f"   📈 {period_name}: {sign}{inf}%")
        else:
            print(f"   ⚠️ {period_name}: not enough data")
    print("---\n")