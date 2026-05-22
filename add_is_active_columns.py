import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def add_is_active():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check and add for 'sheet' table
    cursor.execute("PRAGMA table_info(sheet)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'is_active' not in columns:
        cursor.execute("ALTER TABLE sheet ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print("Added is_active to 'sheet' table")
    else:
        print("is_active already exists in 'sheet' table")

    # Check and add for 'product_sheet' table
    cursor.execute("PRAGMA table_info(product_sheet)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'is_active' not in columns:
        cursor.execute("ALTER TABLE product_sheet ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print("Added is_active to 'product_sheet' table")
    else:
        print("is_active already exists in 'product_sheet' table")

    conn.commit()
    conn.close()
    print("✅ is_active columns check completed.")

if __name__ == '__main__':
    add_is_active()