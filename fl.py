from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)


model = joblib.load("trans_check.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:

        transaction_data = request.form.to_dict()
        df = pd.DataFrame([transaction_data])

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        prediction = model.predict(df)
        fraud_status = "Fraudulent" if prediction[0] == 1 else "Legitimate"
        
        return jsonify({"fraud_status": fraud_status})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
