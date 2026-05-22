import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def add_reset_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(user)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'reset_token' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)")
        print("Added column 'reset_token'")
    if 'token_expiry' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN token_expiry TIMESTAMP")
        print("Added column 'token_expiry'")
    conn.commit()
    conn.close()
    print("✅ Reset columns added successfully.")

if __name__ == '__main__':
    add_reset_columns()