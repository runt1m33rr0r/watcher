import cv2
import threading
from time import sleep
from .processing import ImageProcessor
from .api import register_camera


class Camera(object):
    _frame = None
    _thread = None
    _process_this_frame = True

    @classmethod
    def initialize(cls):
        if cls._thread is None:
            ImageProcessor.init()
            cls._thread = threading.Thread(target=cls._run_camera)
            cls._thread.start()

            while cls.get_frame() is None:
                sleep(0.1)

            register_camera()
        
    @classmethod
    def get_frame(cls):
        return cls._frame

    @classmethod
    def _run_camera(cls):
        video = cv2.VideoCapture(0)

        if not video.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            success, image = video.read()

            if not success:
                continue

            if cls._process_this_frame:
                cls._frame = ImageProcessor.process_video_frame(image)

            cls._process_this_frame = not cls._process_this_frame
