from flask import Flask, render_template, request, jsonify
import subprocess
import threading

app = Flask(__name__)

# Global variable to store the process running the Python script
process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    # return render_template('index.html')
    return render_template('detection page.html')

@app.route('/start_liveness', methods=['POST'])
def start_liveness():
    global process
    if process is None:
        # Start the Python script in a separate thread
        def run_script():
            global process
            process = subprocess.Popen(['python', 'Face_liveness/run.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            process = None  # Reset the process after it finishes

        threading.Thread(target=run_script).start()
        return jsonify({'status': 'success', 'message': 'Liveness testing started.'})
    return jsonify({'status': 'error', 'message': 'Liveness testing is already running.'})

@app.route('/stop_liveness', methods=['POST'])
def stop_liveness():
    global process
    if process is not None:
        process.terminate()  # Terminate the running process
        process = None
        return jsonify({'status': 'success', 'message': 'Liveness testing stopped.'})
    return jsonify({'status': 'error', 'message': 'No liveness testing process is running.'})

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, Response, render_template
# import cv2

# app = Flask(__name__)

# # Function to generate video frames
# def generate_frames():
#     cap = cv2.VideoCapture(0)  # Open the webcam
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Encode the frame as JPEG
#         _, buffer = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

#     cap.release()

# # Route to serve the video feed
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # Route to render the main HTML page
# @app.route('/')
# def index():
#     # return render_template('index.html')
#     return render_template('detection page.html')

# if __name__ == '__main__':
#     app.run(debug=True)