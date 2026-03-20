import sqlite3
from flask import g, current_app

DATABASE = None

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            merchant TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            category TEXT
        );
    """)
    conn.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.config.setdefault('DATABASE', 'transactions.db')
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

if __name__ == '__main__':
    # This part is for standalone database initialization, not used by Flask app
    # For standalone use, we still want to close the connection
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            merchant TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            category TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")
