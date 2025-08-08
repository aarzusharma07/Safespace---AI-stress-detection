from flask import Flask, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stress_detection_db"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_data')
def get_all_data():
    query = """
        SELECT webcam_emotion, voice_stress, survey_stress, created_at
        FROM detection_results
        ORDER BY created_at DESC
        LIMIT 2
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cleaned_results = []
    for row in results:
        # Convert each column to string, especially datetime
        cleaned_row = [str(col) if col is not None else "" for col in row]
        cleaned_results.append(cleaned_row)
    return jsonify(cleaned_results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
