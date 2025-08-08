from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.models import load_model
from moviepy.editor import AudioFileClip
from custom_objects import sum_over_time, sum_shape

app = Flask(__name__)

# Load your Keras model
model = load_model("voice_stress_final.keras", custom_objects={
    'sum_over_time': sum_over_time,
    'sum_shape': sum_shape
})

SR = 22050
N_MFCC = 40
MAX_LEN = 300

# Function to extract MFCC features
def extract_mfcc(audio, sr=SR, n_mfcc=N_MFCC, max_len=MAX_LEN):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    mfcc = mfcc.T
    if mfcc.shape[0] > max_len:
        mfcc = mfcc[:max_len]
    else:
        pad_width = max_len - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0, pad_width), (0, 0)), mode='constant')
    return mfcc

# Route for the UI
@app.route('/')
def home():
    return render_template('voice.html')

# Route to handle voice detection
@app.route('/detect_voice', methods=['POST'])
def detect_voice():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    try:
        audio_file = request.files['audio']
        input_path = "temp.webm"
        output_path = "temp.wav"

        # Save uploaded file as .webm
        audio_file.save(input_path)

        # Convert .webm to .wav using moviepy
        audioclip = AudioFileClip(input_path)
        audioclip.write_audiofile(output_path, codec='pcm_s16le')  # WAV format

        # Load audio and extract MFCC
        y, sr = librosa.load(output_path, sr=SR)
        mfcc = extract_mfcc(y)
        X_input = np.expand_dims(mfcc, axis=0)

        # Predict using the model
        prediction = model.predict(X_input)
        predicted_label = int(prediction[0][0] > 0.5)
        label_text = "Stressed" if predicted_label == 1 else "Non-Stressed"
        confidence = float(prediction[0][0]) if predicted_label == 1 else 1 - float(prediction[0][0])

        return jsonify({
            "stress": label_text,
            "confidence": f"{confidence:.2%}"
        })

    except Exception as e:
        print("🔥 Backend error:", str(e))
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
