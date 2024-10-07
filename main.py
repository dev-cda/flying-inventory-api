import cv2
import sys
from flask import Flask, render_template, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from videostream import VideoStream
from loguru import logger
import time
import threading

logger.info("Starting Flask server...")

app = Flask(__name__)
socketio = SocketIO(app)

logger.info("Flask server started!")

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

@app.route('/')
def index():
    logger.info("Rendering index.html")
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        if camera.stopped:
            break
        frame, qr_code_data = camera.read_qr()
        
        ret, jpeg = cv2.imencode('.jpg',frame)
        
        if len(qr_code_data) >= 2:
            logger.info("Emitting qr_code_data: ", qr_code_data)
            socketio.emit('qr_code_data', qr_code_data)

        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

if __name__ == '__main__':
    from waitress import serve
    # serve(app, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', debug=True, threaded=True)