import sqlite3
from flask import g, current_app

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        # Ensure the database schema is initialized when the first connection is made
        # This is crucial for in-memory databases in tests
        with current_app.app_context():
            init_db() # Call init_db here to ensure tables are created
    return g.db

def init_db():
    # This function now assumes a connection is already available via g.db
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
