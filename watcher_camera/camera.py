import cv2
import threading
from time import sleep


class Camera(object):
    _frame = None
    _thread = None

    def __init__(self):
        if Camera._thread is None:
            Camera._thread = threading.Thread(target=Camera._run_camera)
            Camera._thread.start()

            while Camera.get_frame() is None:
                sleep(0.1)

    @staticmethod
    def get_frame():
        return Camera._frame

    @staticmethod
    def _run_camera():
        video = cv2.VideoCapture(0)

        if not video.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            success, image = video.read()

            if not success:
                continue

            ret, jpeg = cv2.imencode('.jpg', image)

            if not ret:
                continue

            Camera._frame = jpeg.tobytes()
