from flask import Flask, render_template, request, jsonify, session
import torch
import timm
import torchvision.transforms as T
from PIL import Image
import io
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = "super_secret_key"  # For session

# ✅ Simulate login
@app.before_request
def simulate_login_for_now():
    session['user_id'] = 1  # Always user_id = 1

# ✅ DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stress_detection_db"
)
cursor = db.cursor(dictionary=True)

# ✅ Model Load
MODEL_PATH = "swin_emotion_model.pth"
assert os.path.exists(MODEL_PATH), "Model file not found."
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=False, num_classes=len(emotion_labels))
state = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
model.load_state_dict(state)
model.eval()

# ✅ Transform
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize([0.5]*3, [0.5]*3)
])

@app.route('/')
def index():
    return render_template("webcam.html")

# ✅ Webcam Emotion Detection — always insert a NEW row
@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    if 'frame' not in request.files:
        return jsonify({"error": "No frame uploaded"}), 400

    image_file = request.files['frame']
    image_bytes = image_file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    input_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        logits = model(input_tensor)
        pred = torch.argmax(logits, dim=1).item()
        emotion = emotion_labels[pred]
        confidence = float(torch.softmax(logits, dim=1)[0][pred]) * 100

    user_id = session.get('user_id')

    if user_id:
        # ✅ ALWAYS insert a new row for each detection
        cursor.execute("""
            INSERT INTO detection_results (user_id, webcam_emotion, webcam_confidence)
            VALUES (%s, %s, %s)
        """, (user_id, emotion, int(confidence)))
        db.commit()

    return jsonify({
        "emotion": emotion,
        "confidence": int(confidence)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
