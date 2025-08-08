from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging

# Enable debug logs in terminal
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load model once at startup
try:
    model = joblib.load("stress_logreg_model.pkl")
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

# Label mapping
label_map = {
    0: "Normal",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Extremely Severe"
}

@app.route('/predict_stress', methods=['POST'])
def predict_stress():
    try:
        print("✅ Received POST request to /predict_stress")

        data = request.get_json()
        if not data:
            print("❌ No JSON received.")
            return jsonify({"error": "No JSON body received."}), 400

        responses = data.get("responses")
        if not responses or len(responses) != 7:
            print("❌ Invalid or missing 'responses'.")
            return jsonify({"error": "Expected 'responses': list of 7 values."}), 400

        print("📩 Received data:", responses)
        input_array = np.array(responses).reshape(1, -1)

        prediction = model.predict(input_array)[0]
        stress_level = label_map.get(int(prediction), "Unknown")

        print(f"✅ Prediction: {prediction} ({stress_level})")
        return jsonify({
            "predicted_class": int(prediction),
            "stress_level": stress_level
        })

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": str(e)}), 500

# Run the server on all interfaces for local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)

