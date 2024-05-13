const video = document.getElementById('videoElement');
const captureButton = document.getElementById('captureButton');

// Access the webcam stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });

// Function to capture image from webcam
function captureImage() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to data URL
    const dataURL = canvas.toDataURL('image/jpg');
    
    // Create a link element to download the image
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = 'captured_image.jpg';
    link.click();
}

// Event listener for the capture button
captureButton.addEventListener('click', captureImage);