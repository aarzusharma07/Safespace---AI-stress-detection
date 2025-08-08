import cv2
import torch
import timm
import torchvision.transforms as T
from PIL import Image
import numpy as np

# Load pretrained model
print("Loading model...")
model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=True)
model.eval()
print("Model loaded successfully!")

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Preprocess transform
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize([0.5]*3, [0.5]*3)
])

# Open webcam
cap = cv2.VideoCapture(0)  # Try 0 first

if not cap.isOpened():
    print("❌ ERROR: Cannot open webcam. Try changing VideoCapture index.")
    exit()

print("✅ Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame.")
        break

    # Convert to RGB and PIL
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # Preprocess
    input_tensor = transform(img_pil).unsqueeze(0)

    # Predict emotion
    with torch.no_grad():
        logits = model(input_tensor)
        pred = torch.argmax(logits, dim=1).item()
        emotion = emotion_labels[pred % len(emotion_labels)]

# Save to JSON file
with open("emotion.json", "w") as f:
    json.dump({"emotion": emotion}, f)


    # Display on video
    cv2.putText(frame, f'Emotion: {emotion}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Swin Transformer - Emotion Recognition', frame)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
