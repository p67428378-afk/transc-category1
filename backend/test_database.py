import pytest
from flask import Flask, g
import sqlite3 # Import sqlite3 for creating in-memory connection
from .database import init_app, get_db_connection, init_db, close_db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:' # Set the database path for testing
    init_app(app) # Initialize the app with the database config
    
    with app.app_context(): # Establish an app context for the fixture
        init_db() # Initialize the database within this context
    
    yield app # Yield the app for tests to use

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_database_initialization(app):
    with app.app_context(): # This will use the same app context as the fixture
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
        table_exists = cursor.fetchone()
        assert table_exists is not None, "The 'transactions' table should exist after initialization."

def test_get_db_connection(app):
    with app.app_context():
        conn1 = get_db_connection()
        conn2 = get_db_connection()
        assert conn1 is conn2, "get_db_connection should return the same connection within the app context."
