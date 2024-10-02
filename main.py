import cv2
import sys
from flask import Flask, render_template, Response
from videostream import VideoStream
from loguru import logger
import time
import threading

logger.info("Starting Flask server...")
app = Flask(__name__)
logger.info("Flask server started!")

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
        frame = camera.read_qr()
        ret, jpeg = cv2.imencode('.jpg',frame)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)