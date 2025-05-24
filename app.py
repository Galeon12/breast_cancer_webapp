from flask import Flask, render_template, request
import numpy as np
import joblib  # Changed from pickle to joblib

app = Flask(__name__)

# Load model, scaler, and feature names using joblib
model = joblib.load('model.joblib')
scaler = joblib.load('scaler.joblib')
features = joblib.load('features.joblib')

@app.route('/')
def home():
    return render_template('index.html', features=features)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        inputs = [float(request.form.get(feature, 0)) for feature in features]
        print("Inputs:", inputs)
        scaled_inputs = scaler.transform([inputs])
        print("Scaled:", scaled_inputs)
        prediction = model.predict(scaled_inputs)[0]
        print("Prediction:", prediction)
        prob = model.predict_proba(scaled_inputs)
        print("Probabilities:", prob)
        result = 'Malignant (Cancer)' if prediction == 0 else 'Benign (No Cancer)'
        return render_template('index.html', features=features, result=result)
    except Exception as e:
        print("Error:", e)
        return "Prediction failed!"

if __name__ == '__main__':
    app.run(debug=True)