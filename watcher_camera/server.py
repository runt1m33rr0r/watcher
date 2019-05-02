from flask import Flask, Response, render_template
from camera import Camera


app = Flask(__name__)
camera = Camera()


def gen():
    while True:
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + camera.get_frame() + b'\r\n\r\n')


@app.route('/feed')
def feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
