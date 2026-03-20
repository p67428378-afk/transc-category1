from flask import Flask, g, request, jsonify
from .database import get_db_connection, init_app # Removed DATABASE, close_db

app = Flask(__name__)

# Initialize the database for the app
init_app(app)

def get_db():
    return get_db_connection()

@app.route('/api/transactions/upload', methods=['POST'])
def upload_transactions():
    # Placeholder for transaction upload logic
    return jsonify({"message": "Upload endpoint under construction"}), 200

@app.route('/api/reports', methods=['GET'])
def get_reports():
    # Placeholder for report retrieval logic
    return jsonify({"message": "Reports endpoint under construction"}), 200

if __name__ == '__main__':
    app.run(debug=True)
