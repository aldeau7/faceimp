from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import base64

app = Flask(__name__)
socketio = SocketIO(app)

# Your OpenCV face detection logic
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascades/haarcascade_frontalface_default.xml')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_frame')
def handle_frame(frame_data):
    # Process the received frame (e.g., face detection)
    frame = process_frame(frame_data)
    # Encode the frame to base64
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    # Send the processed frame back to the client
    emit('processed_frame', jpg_as_text)

def process_frame(frame_data):
    # Convert base64 string to image array
    jpg_original = base64.b64decode(frame_data)
    nparr = np.frombuffer(jpg_original, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Your face detection logic
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(25, 25))
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return frame

@app.route('/')
def index():
    return render_template('index.html')

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
    socketio.run(app, debug=True)
