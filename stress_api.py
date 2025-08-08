from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load("stress_model.pkl")

@app.route("/predict_stress", methods=["POST"])
def predict():
    data = request.get_json()
    answers = data["answers"]
    
    # Check if we have the expected number of features
    if len(answers) != 21:
        return jsonify({"error": "Expected 21 features"}), 400

    prediction = model.predict([answers])[0]
    return jsonify({"prediction": str(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
