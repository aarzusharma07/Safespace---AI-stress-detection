# SafeSpace — Multimodal AI Stress Detection

A multimodal AI system combining visual, voice, survey, and physiological signals to explore stress detection through machine learning and deep learning.

## Overview
- Webcam-based emotion recognition
- Voice-based stress analysis
- Survey-based prediction
- Heart-rate and respiration sensor data
- Flask backend with browser interfaces

## Architecture
```
Webcam → Swin Transformer ┐
Voice → MFCC + Keras      ├→ Flask Backend → Web UI
Survey → Random Forest    │
Sensors → HR/Respiration ┘
```

## Tech Stack
**Python · Flask · HTML/CSS/JavaScript · Random Forest · Swin Transformer · Keras · MFCC · Arduino**

## Key Components
- `stress_api.py` — Flask backend
- `read_and_predict.py` — inference logic
- `survey.html` — survey interface
- `voice.html` — voice interface
- `webcam.html` — webcam interface

## Running Locally
```bash
pip install -r requirements.txt
python stress_api.py
```

> Experimental ML project for educational purposes; not a clinical diagnostic tool.

---

Maintained by **Aarzu Sharma** | Computer Engineering