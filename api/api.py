from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import joblib
import numpy as np
import os

# E:\c++\ML\ML Final Boss\yt\credit_card\api\api.py
app = Flask(__name__)
CORS(app)  # Allows independent frontend files to securely send cross-origin requests

# Explicit feature signature matching your model's requirement
FEATURE_NAMES = ['V1', 'V2', 'V3', 'V4', 'V5', 'V7', 'V9', 'V10', 'V11', 'V12', 'V14', 'V16', 'V17', 'V18']
MODEL_PATH = 'E:/c++/ML/ML Final Boss/yt/credit_card/model/fraud_model.pkl'

def load_model_once():
    """Reads the binary file into memory only once at initialization."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Missing required model file: {MODEL_PATH}")
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return joblib.load(MODEL_PATH)

# Global Assignment: Runs immediately when the script executes
print("--- Loading ML Model into Server Memory ---")
MODEL = load_model_once()
print("--- Model Cached in RAM. Pure API Endpoint Ready ---")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'Malformed request body. Expected a "features" key.'}), 400
        
        input_features = data['features']
        
        # Guard clause: shape validation
        if len(input_features) != len(FEATURE_NAMES):
            return jsonify({'error': f'Dimension mismatch. Expected {len(FEATURE_NAMES)} features, received {len(input_features)}.'}), 400

        # Type conversion guard
        try:
            processed_features = [float(val) for val in input_features]
        except (ValueError, TypeError):
            return jsonify({'error': 'All incoming features must be numeric floating-point values.'}), 400

        # Convert to 2D numpy array: shape (1, 14)
        input_matrix = np.array(processed_features).reshape(1, -1)
        
        # Inference using the global cached model object in RAM
        prediction = int(MODEL.predict(input_matrix)[0])
        probabilities = MODEL.predict_proba(input_matrix)[0]
        fraud_probability = float(probabilities[1])

        return jsonify({
            'prediction': prediction,
            'is_fraud': bool(prediction == 1),
            'fraud_probability': fraud_probability
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal Server Processing Exception: {str(e)}'}), 500


if __name__ == '__main__':
    # Starts server on http://127.0.0.1:5000/predict
    app.run(debug=True)