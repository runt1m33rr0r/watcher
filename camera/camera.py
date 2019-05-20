import cv2
import threading
from time import sleep
import camera.processing as processing


frame = None
_thread = None
_process_this_frame = True


def _run_camera():
    global _process_this_frame
    global frame

    video = cv2.VideoCapture(0)

    if not video.isOpened():
        raise RuntimeError('Could not start camera.')

    while True:
        success, image = video.read()

        if not success:
            continue

        if _process_this_frame:
            frame = processing.process_video_frame(image)


        _process_this_frame = not _process_this_frame


def init():
    global _thread

    if _thread is None:
        processing.init()
        _thread = threading.Thread(target=_run_camera)
        _thread.start()

        while frame is None:
            sleep(0.1)