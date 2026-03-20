from flask import Flask, g, request, jsonify
from .database import init_db, get_db_connection, DATABASE

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = get_db_connection()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/api/transactions/upload', methods=['POST'])
def upload_transactions():
    # Placeholder for transaction upload logic
    return jsonify({"message": "Upload endpoint under construction"}), 200

@app.route('/api/reports', methods=['GET'])
def get_reports():
    # Placeholder for report retrieval logic
    return jsonify({"message": "Reports endpoint under construction"}), 200

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)