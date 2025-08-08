from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ✅ DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stress_detection_db"
)
cursor = db.cursor()

# ✅ Route: Submit survey
@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    data = request.get_json()
    if not data or "answers" not in data:
        return jsonify({"error": "No data received"}), 400

    answers = data["answers"]
    total = sum(answers)
    percent = (total / 75) * 100

    if percent <= 33:
        level = "Low"
    elif percent <= 66:
        level = "Moderate"
    else:
        level = "High"

    try:
        # Update latest record for user_id = 1
        cursor.execute("""
            UPDATE detection_results
            SET survey_stress = %s
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (level, 1))
        db.commit()

        return jsonify({
            "status": "success",
            "total": total,
            "percent": round(percent, 2),
            "level": level
        })
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Route: Serve survey.html
@app.route('/')
def serve_html():
    return send_from_directory(app.static_folder, 'survey.html')

# ✅ NEW Route: Fetch latest combined stress prediction
@app.route('/latest_combined', methods=['GET'])
def latest_combined():
    try:
        cursor.execute("""
            SELECT webcam_emotion, webcam_confidence, voice_stress, voice_confidence,
                   survey_stress, created_at
            FROM detection_results
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (1,))
        row = cursor.fetchone()

        if row:
            return jsonify({
                "webcam_emotion": row[0],
                "webcam_confidence": row[1],
                "voice_stress": row[2],
                "voice_confidence": row[3],
                "survey_stress": row[4],
                "created_at": str(row[5])
            })
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
