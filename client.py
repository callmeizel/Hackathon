from flask import Flask, jsonify
import sqlite3
import pandas as pd
import joblib
import time

app = Flask(__name__)

model, scaler = joblib.load("trans_check.pkl")


def get_unprocessed_transactions():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE processed = 0")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def mark_transaction_as_processed(transaction_id, fraud_level, fraud_probability):
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET processed = 1
        WHERE id = ?
    ''', (transaction_id,))
    conn.commit()
    conn.close()

def process_transactions():
    transactions = get_unprocessed_transactions()
    results = []

    for transaction in transactions:
        transaction_id, acc_id, acc_num, category, amount, processed = transaction
        trans_df = pd.DataFrame([{"acc_id": acc_id, "acc_num": acc_num, "category": category, "amount": amount}])

        prediction_proba = model.predict_proba(trans_df)[0][1] * 100
        
       
        if prediction_proba <= 25:
            fraud_level = "Low"
        elif 30 <= prediction_proba <= 69:
            fraud_level = "Mid"
        elif 70 <= prediction_proba <= 85:
            fraud_level = "High"
        else:
            fraud_level = "Very High"
        
        
        mark_transaction_as_processed(transaction_id, fraud_level, prediction_proba)

       
        results.append({
            "transaction_id": transaction_id,
            "fraud_level": fraud_level,
            "fraud_probability": f"{prediction_proba:.2f}%"
        })

    return results


@app.route('/')
def home():
    return jsonify({"message": "Fraud Detection API is running!"})

@app.route('/process_transactions', methods=['GET'])
def process_transactions_route():
    results = process_transactions()
    return jsonify(results if results else {"message": "No new transactions to process."})

if __name__ == '__main__':
    app.run(debug=True)
