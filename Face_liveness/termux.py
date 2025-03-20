import cv2
import numpy as np
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array

# Load your pre-trained model
try:
    model = load_model("face_antispoofing_model.h5")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Define the threshold for classification
threshold = 0.2

# API endpoint for Termux (change IP)
API_URL = "http://192.0.0.4:5000/get_status"  # Replace with Termux IP

def get_termux_status():
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json().get("status", "True")  # Default to "True"
    except requests.exceptions.RequestException:
        print("Error: Unable to connect to Termux API")
    return "True"  # Default value if API fails

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to exit.")

cv2.namedWindow("Live Camera Feed", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Live Camera Feed", 800, 600)
cv2.setWindowProperty("Live Camera Feed", cv2.WND_PROP_TOPMOST, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize the frame to match model input size
    resized_frame = cv2.resize(frame, (224, 224))
    image_array = img_to_array(resized_frame) / 255.0  # Normalize

    # Predict using the model
    prediction = model.predict(np.expand_dims(image_array, axis=0))[0]
    liveness_score = prediction[0]

    # Get Termux decision
    termux_status = get_termux_status()
    
    # Override prediction if Termux status is "False"
    if termux_status == "False":
        liveness_score = 1.0  # Force fake result

    # Determine label
    label = "Live Image" if liveness_score <= threshold else "Not Live Image - Spoofed"

    # Display label
    cv2.putText(frame, f"{label} (Score: {liveness_score:.2f})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if label == "Live Image" else (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Live Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
