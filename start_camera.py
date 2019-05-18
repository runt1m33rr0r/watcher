import sys
from flask import Flask, Response
import camera.camera as camera
from time import sleep
from camera.api import set_camera_city, set_camera_name, set_central_server, set_camera_host, set_camera_port


app = Flask(__name__)


def gen():
    while True:
        sleep(0.1)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + camera.frame + b'\r\n\r\n')


@app.route('/')
def index():
    return 'hello'


@app.route('/feed')
def feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    user_input = sys.argv[1:]

    if len(user_input) < 5:
        print('Not enough arguments: 1. central server url, 2. camera name, 3. city name, 4. camera ip, 5. camera port')
        exit()

    central_server = user_input[0].rstrip('/')
    camera_name = user_input[1]
    city_name = user_input[2]
    host = user_input[3]
    port = int(user_input[4])

    set_central_server(central_server)
    set_camera_name(camera_name)
    set_camera_city(city_name)
    set_camera_host(host)
    set_camera_port(port)

    camera.init()

    app.run(host=host, threaded=True, port=int(port))