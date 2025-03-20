console.log('Hello, World!');

// const videoElement = document.getElementById('camera-feed');
// const startCameraButton = document.getElementById('start-camera-btn');
// const stopCameraButton = document.getElementById('stop-camera-btn');

// let stream;

// // Function to start the camera
// async function startCamera() {
//     try {
//         stream = await navigator.mediaDevices.getUserMedia({ video: true });
//         videoElement.srcObject = stream;
//         startCameraButton.disabled = true; // Disable the start button
//         stopCameraButton.disabled = false; // Enable the stop button
//     } catch (error) {
//         console.error('Error accessing the camera:', error);
//         alert('Unable to access the camera. Please check your permissions.');
//     }
// }

// // Function to stop the camera
// function stopCamera() {
//     if (stream) {
//         const tracks = stream.getTracks();
//         tracks.forEach(track => track.stop());
//         videoElement.srcObject = null;
//         startCameraButton.disabled = false; // Enable the start button
//         stopCameraButton.disabled = true; // Disable the stop button
//     }
// }

// // Event listeners for the buttons
// startCameraButton.addEventListener('click', startCamera);
// stopCameraButton.addEventListener('click', stopCamera);

const startLivenessButton = document.getElementById('start-liveness-btn');
const stopLivenessButton = document.getElementById('stop-liveness-btn');
const videoElement = document.getElementById('camera-feed');

let stream;

// Function to start the camera and notify the server to run the Python script
async function startLivenessTesting() {
    try {
        // Start the webcam feed
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;

        // Notify the server to start the Python script
        const response = await fetch('/start_liveness', { method: 'POST' });
        if (response.ok) {
            console.log("Liveness testing started.");
            startLivenessButton.disabled = true;
            stopLivenessButton.disabled = false;
        } else {
            alert("Failed to start liveness testing.");
        }
    } catch (error) {
        console.error('Error accessing the camera:', error);
        alert('Unable to access the camera. Please check your permissions.');
    }
}

// Function to stop the camera and notify the server to stop the Python script
function stopLivenessTesting() {
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        videoElement.srcObject = null;

        // Notify the server to stop the Python script
        fetch('/stop_liveness', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    console.log("Liveness testing stopped.");
                    startLivenessButton.disabled = false;
                    stopLivenessButton.disabled = true;
                } else {
                    alert("Failed to stop liveness testing.");
                }
            });
    }
}

// Event listeners for the buttons
startLivenessButton.addEventListener('click', startLivenessTesting);
stopLivenessButton.addEventListener('click', stopLivenessTesting);

// Get the "Get Started" button by its ID
const getStartedButton = document.getElementById('get-started-btn');

// Add a click event listener to the button
getStartedButton.addEventListener('click', () => {
    // Redirect to the '/detection' route
    window.location.href = '/detection';
  });