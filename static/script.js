// Function to capture image from the video feed
function captureImage() {
    const img = document.getElementById('bg');
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const context = canvas.getContext('2d');
    context.drawImage(img, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to data URL
    const dataURL = canvas.toDataURL('image/png');
    
    // Create a link element to download the image
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = 'captured_image.png';
    link.click();
}

// Event listener for the capture button
const captureButton = document.getElementById('captureButton');
captureButton.addEventListener('click', captureImage);
