import sqlite3
from datetime import datetime

DATABASE = 'transactions.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                date TEXT NOT NULL,
                merchant TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                upload_timestamp TEXT NOT NULL,
                original_csv_row TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorized_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_transaction_id INTEGER NOT NULL,
                user_id TEXT,
                date TEXT NOT NULL,
                merchant TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                category_id INTEGER,
                categorization_timestamp TEXT NOT NULL,
                FOREIGN KEY (raw_transaction_id) REFERENCES raw_transactions(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        # Insert predefined categories if they don't exist
        categories = ["Food", "Rent", "Bills", "Shopping", "Miscellaneous", "Utilities"]
        for category in categories:
            try:
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
            except sqlite3.IntegrityError:
                # Category already exists
                pass
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    init_db()
    print("Database initialized with tables and default categories.")
