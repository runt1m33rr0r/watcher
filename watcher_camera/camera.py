import cv2
import threading
from time import sleep
from processing import process_video_frame
from api import register_camera, update_classifier


class Camera(object):
    _frame = None
    _thread = None


    @staticmethod
    def initialize():
        if Camera._thread is None:
            Camera._thread = threading.Thread(target=Camera._run_camera)
            Camera._thread.start()

            while Camera.get_frame() is None:
                sleep(0.1)

            register_camera()
            update_classifier()
        

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

            Camera._frame = process_video_frame(image)

