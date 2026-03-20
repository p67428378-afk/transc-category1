import sqlite3
from flask import g

DATABASE = None

def get_db_connection(database_path=None):
    global DATABASE
    if database_path is None:
        database_path = DATABASE
    
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(database_path=None):
    conn = get_db_connection(database_path)
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
    return conn # Return the connection for further use, especially in tests

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app, database_path='transactions.db'):
    global DATABASE
    DATABASE = database_path
    app.teardown_appcontext(close_db)
    with app.app_context():
        conn = init_db(database_path)
        conn.close() # Close the connection after initialization in app context

if __name__ == '__main__':
    # This part is for standalone database initialization, not used by Flask app
    # For standalone use, we still want to close the connection
    conn = init_db('transactions.db')
    conn.close()
    print("Database initialized.")
