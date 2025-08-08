from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import mysql.connector
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
CORS(app)

# ✅ Load ML model
try:
    model = joblib.load("stress_logreg_model.pkl")
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

# ✅ Stress label mapping
label_map = {
    0: "Normal",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Extremely Severe"
}

# ✅ Connect to MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stress_detection_db"
    )
    cursor = db.cursor()
    print("✅ Connected to MySQL database.")
except Exception as e:
    print("❌ DB connection error:", e)
    db = None
    cursor = None

# ✅ Serve the HTML form
@app.route('/')
def serve_form():
    return send_from_directory('.', 'stress_form.html')

# ✅ Stress prediction API
@app.route('/predict_stress', methods=['POST'])
def predict_stress():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received."}), 400

        responses = data.get("responses")
        if not responses or len(responses) != 7:
            return jsonify({"error": "Expected 7 responses"}), 400

        input_array = np.array(responses).reshape(1, -1)
        prediction = model.predict(input_array)[0]
        stress_level = label_map.get(int(prediction), "Unknown")

        # ✅ Insert new record into database
        if cursor:
            cursor.execute("""
                INSERT INTO detection_results (user_id, survey_stress, created_at)
                VALUES (%s, %s, NOW())
            """, (1, stress_level))
            db.commit()
            print("✅ Inserted stress level into DB:", stress_level)

        return jsonify({
            "predicted_class": int(prediction),
            "stress_level": stress_level
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)
