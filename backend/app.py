import csv
import io
import json
from datetime import datetime

from flask import Flask, request, jsonify, g
from flask_cors import CORS

from database import init_db, get_db_connection, DATABASE
from llm_categorizer import LLMCategorizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

llm_categorizer = LLMCategorizer()

def get_db():
    if 'db' not in g:
        g.db = get_db_connection()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.before_request
def before_request():
    init_db() # Ensure DB is initialized before each request

@app.route('/api/transactions/upload', methods=['POST'])
def upload_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400

    db = get_db()
    cursor = db.cursor()
    upload_timestamp = datetime.now().isoformat()
    user_id = request.form.get('user_id', 'default_user') # Placeholder for user ID

    csv_file = io.TextIOWrapper(file.stream, encoding='utf-8')
    reader = csv.DictReader(csv_file)
    transactions_processed = 0
    transactions_categorized = 0

    # Fetch category IDs once
    category_names_to_ids = {}
    for row in cursor.execute("SELECT id, name FROM categories").fetchall():
        category_names_to_ids[row['name']] = row['id']

    for row in reader:
        # Basic cleaning and validation
        try:
            date = row.get('Date')
            merchant = row.get('Merchant')
            amount = float(row.get('Amount'))
            description = row.get('Description', '')

            if not all([date, merchant, amount is not None]):
                print(f"Skipping row due to missing data: {row}")
                continue

            original_csv_row = json.dumps(row) # Store original row for deduplication check

            # Deduplication based on 'merchant' field only
            cursor.execute(
                "SELECT id FROM raw_transactions WHERE merchant = ? AND original_csv_row = ?",
                (merchant, original_csv_row)
            )
            existing_raw_transaction = cursor.fetchone()

            raw_transaction_id = None
            if existing_raw_transaction:
                raw_transaction_id = existing_raw_transaction['id']
                print(f"Skipping duplicate raw transaction for merchant {merchant}.")
            else:
                cursor.execute(
                    "INSERT INTO raw_transactions (user_id, date, merchant, amount, description, upload_timestamp, original_csv_row) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, date, merchant, amount, description, upload_timestamp, original_csv_row)
                )
                raw_transaction_id = cursor.lastrowid
                transactions_processed += 1

            # Categorize and store in categorized_transactions table
            if raw_transaction_id:
                # Check if this specific raw_transaction_id has already been categorized
                cursor.execute(
                    "SELECT id FROM categorized_transactions WHERE raw_transaction_id = ?",
                    (raw_transaction_id,)
                )
                if cursor.fetchone():
                    print(f"Transaction {raw_transaction_id} already categorized. Skipping.")
                    continue

                predicted_category_name = llm_categorizer.categorize(merchant, description)
                category_id = category_names_to_ids.get(predicted_category_name)

                if category_id:
                    cursor.execute(
                        "INSERT INTO categorized_transactions (raw_transaction_id, user_id, date, merchant, amount, description, category_id, categorization_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (raw_transaction_id, user_id, date, merchant, amount, description, category_id, datetime.now().isoformat())
                    )
                    transactions_categorized += 1
                else:
                    print(f"Warning: Category '{predicted_category_name}' not found for transaction {raw_transaction_id}")

        except (ValueError, KeyError) as e:
            print(f"Error processing row {row}: {e}")
            continue
    db.commit()

    return jsonify({
        "message": "Transactions uploaded and processed",
        "transactions_processed": transactions_processed,
        "transactions_categorized": transactions_categorized
    }), 200

@app.route('/api/reports', methods=['GET'])
def get_reports():
    db = get_db()
    cursor = db.cursor()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_name = request.args.get('category')
    user_id = request.args.get('user_id', 'default_user') # Placeholder for user ID

    query = """
        SELECT
            ct.date, ct.merchant, ct.amount, ct.description, c.name as category
        FROM
            categorized_transactions ct
        JOIN
            categories c ON ct.category_id = c.id
        WHERE
            ct.user_id = ?
    """
    params = [user_id]

    if start_date:
        query += " AND ct.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND ct.date <= ?"
        params.append(end_date)
    if category_name:
        query += " AND c.name = ?"
        params.append(category_name)

    cursor.execute(query, params)
    reports = [dict(row) for row in cursor.fetchall()]

    return jsonify(reports), 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM categories")
    categories = [row['name'] for row in cursor.fetchall()]
    return jsonify(categories), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
