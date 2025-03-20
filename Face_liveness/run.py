import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array

# Load your pre-trained model
try:
    model = load_model("face_antispoofing_model.h5")
    print("Model loaded successfully.")
    print(f"Model input shape: {model.input_shape}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Define the threshold for classification
threshold = 0.8  # Adjust this value based on your model's performance

# Open the webcam
cap = cv2.VideoCapture(1)  # Change 0 to the index of your camera if you have multiple cameras
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to exit the live feed.")

# Create a named window and set its size
cv2.namedWindow("Live Camera Feed", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Live Camera Feed", 800, 600)  # Set the desired width and height
cv2.setWindowProperty("Live Camera Feed", cv2.WND_PROP_TOPMOST, 1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize the frame to the required input size of the model (224x224)
    resized_frame = cv2.resize(frame, (224, 224))
    image_array = img_to_array(resized_frame)
    image_array /= 255.0  # Normalize the image to [0, 1]

    # Predict using the model
    prediction = model.predict(np.expand_dims(image_array, axis=0))[0]
    print(f"Prediction: {prediction}")

    liveness_score = prediction[0]
    # Determine the label based on the threshold
    label = "Live Image" if liveness_score <= threshold else "Not Live Image - Spoofed"

    # Display the prediction on the video feed
    cv2.putText(
        frame,
        f"{label} (Score: {liveness_score:.2f})",
        (10, 30),  # Position of text
        cv2.FONT_HERSHEY_SIMPLEX,  # Font
        1,  # Font scale
        (0, 255, 0) if label == "Live Image" else (0, 0, 255),  # Text color (green for live, red for spoofed)
        2,  # Thickness
        cv2.LINE_AA
    )

    # Show the frame with the prediction
    cv2.imshow("Live Camera Feed", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()


# import cv2
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.utils import img_to_array
# import base64

# # Load your pre-trained model
# try:
#     model = load_model("face_antispoofing_model.h5")
#     print("Model loaded successfully.")
#     print(f"Model input shape: {model.input_shape}")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     exit()

# threshold = 0.8

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not open webcam.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     resized_frame = cv2.resize(frame, (224, 224))
#     image_array = img_to_array(resized_frame)
#     image_array /= 255.0

#     prediction = model.predict(np.expand_dims(image_array, axis=0))[0]
#     liveness_score = prediction[0]
#     label = "Live Image" if liveness_score <= threshold else "Not Live Image - Spoofed"

#     cv2.putText(
#         frame,
#         f"{label} (Score: {liveness_score:.2f})",
#         (10, 30),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1,
#         (0, 255, 0) if label == "Live Image" else (0, 0, 255),
#         2,
#         cv2.LINE_AA
#     )

#     # Encode the frame as a JPEG image
#     _, buffer = cv2.imencode('.jpg', frame)
#     frame_base64 = base64.b64encode(buffer).decode('utf-8')

#     # Send the frame to the Flask backend (or directly to the frontend via WebSocket)
#     print(frame_base64)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()