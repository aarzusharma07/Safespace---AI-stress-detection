from flask import Flask, render_template, jsonify
import cv2, threading, torch, timm
import torchvision.transforms as T
from PIL import Image

app = Flask(__name__)

# Load pretrained Swin Transformer model
model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=True)
model.eval()
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize([0.5]*3, [0.5]*3)
])

# Shared state
current_emotion = {'emotion': '--'}
detecting = False

def detect_emotion():
    global current_emotion, detecting
    cap = cv2.VideoCapture(0)
    while detecting:
        ret, frame = cap.read()
        if not ret:
            continue
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(tensor)
            pred = torch.argmax(output, dim=1).item()
            current_emotion['emotion'] = emotion_labels[pred % len(emotion_labels)]
    cap.release()

@app.route('/')
def home():
    return render_template('webcam.html')

@app.route('/start')
def start_detection():
    global detecting
    if not detecting:
        detecting = True
        thread = threading.Thread(target=detect_emotion)
        thread.start()
    return "Detection started"

@app.route('/emotion')
def get_emotion():
    return jsonify(current_emotion)

if __name__ == '__main__':
    app.run(debug=True)
#venv\Scripts\activate