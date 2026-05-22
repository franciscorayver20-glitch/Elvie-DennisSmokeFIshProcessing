# add_constraint.py
import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def add_unique_constraint():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Remove duplicate (sheet_id, product_id) pairs, keep the one with smallest id
    print("Removing duplicate entries...")
    cursor.execute('''
        DELETE FROM sheet_product
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM sheet_product
            GROUP BY sheet_id, product_id
        )
    ''')
    print(f"Deleted {cursor.rowcount} duplicate rows.")
    
    # Commit the DELETE operation to close implicit transaction
    conn.commit()

    # 2. Now add the unique constraint by recreating the table
    # Disable foreign keys
    cursor.execute("PRAGMA foreign_keys=OFF;")
    # Start explicit transaction
    cursor.execute("BEGIN TRANSACTION;")

    cursor.execute('''
        CREATE TABLE sheet_product_new (
            id INTEGER PRIMARY KEY,
            sheet_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            status VARCHAR(50),
            last_modified DATETIME,
            UNIQUE(sheet_id, product_id)
        )
    ''')

    cursor.execute('''
        INSERT INTO sheet_product_new (id, sheet_id, product_id, stock, status, last_modified)
        SELECT id, sheet_id, product_id, stock, status, last_modified FROM sheet_product
    ''')

    cursor.execute('DROP TABLE sheet_product')
    cursor.execute('ALTER TABLE sheet_product_new RENAME TO sheet_product')

    # Re-enable foreign keys
    cursor.execute("PRAGMA foreign_keys=ON;")
    conn.commit()
    conn.close()
    print("✅ Unique constraint added successfully.")

if __name__ == '__main__':
    add_unique_constraint()