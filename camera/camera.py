import cv2
import threading
from time import sleep
from api import register_camera
from processing import ImageProcessor


class Camera(object):
    _frame = None
    _thread = None
    _process_this_frame = True

    @staticmethod
    def initialize():
        if Camera._thread is None:
            ImageProcessor.initialize()
            Camera._thread = threading.Thread(target=Camera._run_camera)
            Camera._thread.start()

            while Camera.get_frame() is None:
                sleep(0.1)

            register_camera()
        
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

            if Camera._process_this_frame:
                Camera._frame = ImageProcessor.process_video_frame(image)

            Camera._process_this_frame = not Camera._process_this_frame
