# Safespace---AI-stress-detection
Multimodal AI stress detection using webcam-based emotion recognition (Swin Transformer), voice analysis (Keras), survey response (RandomForest), and hardware inputs (heart/respiration rate via sensors). Built with Flask, JS, ML/DL models, and real-time browser UI.


# Stress Detection System using AI & Bio-sensors

An integrated stress detection system using Machine Learning, Deep Learning, and bio-sensor data (heart rate and respiration rate). The system includes a live webcam-based emotion detector, a survey-based stress predictor, and hardware interfacing for physiological data.

## 🔧 Features
- 🎭 Emotion Detection using Webcam (Swin Transformer)
- 📋 Survey-based Stress Prediction (Random Forest)
- 🎙️ Voice-based Stress Prediction (Keras + MFCC)
- ❤️ Hardware-based Detection using Heart Rate & Respiration Sensors
- 📊 Real-time prediction with Flask API & interactive UI

## 🧠 Tech Stack
- Python, Flask, HTML/CSS/JS
- Machine Learning (RandomForest)
- Deep Learning (Swin Transformer, Keras)
- SoundDevice, MFCC, MoviePy
- Arduino / IoT sensor integration

## 🗂️ Project Structure
- `stress_model.pkl` – Survey stress prediction model
- `voice_stress_final.keras` – Voice stress detection model
- `swin_emotion_model.pth` – Emotion detection model
- `stress_api.py`, `read_and_predict.py` – Flask backend scripts
- `survey.html`, `voice.html`, `webcam.html` – Frontend pages

## 🧪 How to Run
1. Clone the repo
2. Install dependencies (`pip install -r requirements.txt`)
3. Run Flask backend:
    ```bash
    python stress_api.py
    ```
4. Open `survey.html`, `voice.html`, or `webcam.html` in browser
5. For hardware, connect Arduino and run serial reader code

## 📝 Dataset
- Survey Dataset (Kaggle)
- Voice Stress Audio (Custom)
- Emotion Detection Images (FER-2013 or custom)


## 📷 Screenshots

<img width="1221" height="786" alt="image" src="https://github.com/user-attachments/assets/d7eadfb1-996c-4eb3-82e5-f3afa45c67cd" />




