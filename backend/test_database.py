import pytest
from flask import Flask, g
import sqlite3 # Import sqlite3 for creating in-memory connection
from .database import init_app, get_db_connection, init_db, close_db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Create a single in-memory database connection for the test suite
    test_conn = sqlite3.connect(':memory:')
    test_conn.row_factory = sqlite3.Row

    init_app(app, test_db_connection=test_conn) # Pass the test connection to init_app
    
    yield app
    
    # Ensure the test connection is closed after tests
    test_conn.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_database_initialization(app):
    with app.app_context():
        conn = get_db_connection() # This will now return the test_conn
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
        table_exists = cursor.fetchone()
        assert table_exists is not None, "The 'transactions' table should exist after initialization."

def test_get_db_connection(app):
    with app.app_context():
        conn1 = get_db_connection()
        conn2 = get_db_connection()
        assert conn1 is conn2, "get_db_connection should return the same connection within the app context."
