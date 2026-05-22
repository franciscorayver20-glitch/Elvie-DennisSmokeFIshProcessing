import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def add_all_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(user)")
    columns = [col[1] for col in cursor.fetchall()]

    # Add date_created if missing
    if 'date_created' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN date_created TIMESTAMP")
        print("Added column 'date_created' (NULL for existing rows)")

    # Add last_login if missing
    if 'last_login' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN last_login TIMESTAMP")
        print("Added column 'last_login'")

    # Add is_online if missing
    if 'is_online' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN is_online INTEGER DEFAULT 0")
        print("Added column 'is_online'")

    # Add last_updated if missing
    if 'last_updated' not in columns:
        cursor.execute("ALTER TABLE user ADD COLUMN last_updated TIMESTAMP")
        print("Added column 'last_updated'")

    conn.commit()
    conn.close()
    print("✅ All missing columns added successfully.")

if __name__ == '__main__':
    add_all_columns()