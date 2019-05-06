from flask import Flask, Response
from camera import Camera
from time import sleep
from api import get_classifier_date


app = Flask(__name__)
Camera.initialize()


def gen():
    while True:
        sleep(0.1)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + Camera.get_frame() + b'\r\n\r\n')


@app.route('/feed')
def feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
