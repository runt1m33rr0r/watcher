import cv2
from PIL import Image
from io import BytesIO
from .api import alert, update, get_settings, get_classifier
import face_recognition
from time import sleep
import threading
from common.ai import draw_boxes, predict


UNKNOWN = 'unknown'

_can_process = False
_updater_thread = None
_update_timeout = 300
_settings = None
_downscale = None
_sensitivity = 0.55


def _classifier_updater_thread():
    global _can_process
    global _can_process
    global _update_timeout
    global _settings
    global _downscale
    global _sensitivity

    while True:
        print('updating classifier')

        _can_process = False
        update()
        _settings = get_settings()
        _update_timeout = _settings['camera_update_timeout'] * 60
        _sensitivity = _settings['detection_sensitivity']
        _downscale = _settings['downscale_level']
        _can_process = True
        
        sleep(_update_timeout)


def init():
    global _updater_thread

    if not _updater_thread:
        _updater_thread = threading.Thread(target=_classifier_updater_thread)
        _updater_thread.start()


def process_video_frame(frame):
    name = UNKNOWN

    if _can_process:
        prediction = predict(frame, get_classifier(), _downscale, _sensitivity)
        draw_boxes(frame, prediction, _downscale)

        for person in prediction:
            name = person[0]

    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        return

    frame = jpeg.tobytes()

    if name != UNKNOWN:
        alert(name, frame)
    
    return frame
