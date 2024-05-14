
import numpy as np
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Your OpenCV face detection logic
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
profil_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')

def generate_frames():
    camera = cv2.VideoCapture(0)  # Use the default camera
    
    frame_count = 0  # Counter to keep track of frames processed
    
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame from camera")
            break
        else:
            # Increment frame count
            frame_count += 1
            
            # Skip processing if it's not the second frame
            if frame_count % 5 != 0:
                continue

            # Convert the frame to grayscale for face and profilface detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(25, 25))
            
            # Detect profilfaces in the frame
            profils = profil_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))

            # Blur faces excluding the eye areas
            for (x, y, w, h) in faces:
                # Calculate blur radius based on face size
                blur_radius = int(max(w, h) / 10)
                # Ensure blur radius is odd for GaussianBlur
                if blur_radius % 2 == 0:
                    blur_radius += 1
                # Blur the face region
                blurred_face = cv2.GaussianBlur(frame[y:y+h, x:x+w], (blur_radius, blur_radius), 0)
                # Replace the face region with the blurred face
                frame[y:y+h, x:x+w] = blurred_face
                # Generate more rectangles based on the size of the face
                for _ in range(int(((w * w) / 160 - w/2))):  # Adjust the divisor to control rectangle density
                    # Randomly generate rectangle parameters
                    rx = np.random.randint(x, x + w)
                    ry = np.random.randint(y, y + h)
                    rwidth = np.random.randint(2, 20)  # Adjust the range of width here
                    rheight = np.random.randint(2, 20)  # Adjust the range of height here

                    # Generate a random pastel-like color
                    pastel_color = np.random.randint(150, 256, size=(3,), dtype=np.uint8)

                    # Extract the rectangle from the frame
                    rectangle = frame[ry:ry+rheight, rx:rx+rwidth]

                    # Blend the pastel color with the rectangle using element-wise multiplication
                    rectangle[:, :, 0] = cv2.multiply(rectangle[:, :, 0], pastel_color[0] / 255.0)
                    rectangle[:, :, 1] = cv2.multiply(rectangle[:, :, 1], pastel_color[1] / 255.0)
                    rectangle[:, :, 2] = cv2.multiply(rectangle[:, :, 2], pastel_color[2] / 255.0)

            # Generate random rectangles for the entire frame
            for _ in range(64):  # Adjust the number of rectangles here
                # Randomly generate rectangle parameters for the entire frame
                rx = np.random.randint(0, frame.shape[1])
                ry = np.random.randint(0, frame.shape[0])
                rwidth = np.random.randint(2, 100)  # Adjust the range of width here
                rheight = np.random.randint(2, 100)  # Adjust the range of height here

                # Generate a random pastel-like color
                pastel_color = np.random.randint(150, 256, size=(3,), dtype=np.uint8)

                # Extract the rectangle from the frame
                rectangle = frame[ry:ry+rheight, rx:rx+rwidth]

                # Blend the pastel color with the rectangle using element-wise multiplication
                rectangle[:, :, 0] = cv2.multiply(rectangle[:, :, 0], pastel_color[0] / 255.0)
                rectangle[:, :, 1] = cv2.multiply(rectangle[:, :, 1], pastel_color[1] / 255.0)
                rectangle[:, :, 2] = cv2.multiply(rectangle[:, :, 2], pastel_color[2] / 255.0)

            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
