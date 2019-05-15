import cv2
from PIL import Image
from io import BytesIO
from .api import alert, get_classifier, update, settings
import face_recognition
from time import sleep
import threading
from common.ai import draw_boxes, predict


UNKNOWN = 'unknown'


class ImageProcessor(object):
    _can_process = True
    _classifier = None
    _updater_thread = None
    _update_timeout = 300
    _downscale = 2
    _sensitivity = 0.55

    @classmethod
    def init(cls):
        if not cls._updater_thread:
            cls._updater_thread = threading.Thread(target=cls._classifier_updater_thread)
            cls._updater_thread.start()

    @classmethod
    def _classifier_updater_thread(cls):
        while True:
            print('updating classifier')

            cls._can_process = False
            update()
            cls._classifier = get_classifier()
            cls._can_process = True

            cls._update_timeout = settings['camera_update_timeout'] * 60
            cls._downscale = settings['downscale_level']
            cls._sensitivity = settings['detection_sensitivity']

            sleep(cls._update_timeout)

    @classmethod
    def process_video_frame(cls, frame):
        name = UNKNOWN

        if cls._can_process:
            prediction = predict(frame, cls._classifier, cls._downscale, cls._sensitivity)
            draw_boxes(frame, prediction, cls._downscale)

            for person in prediction:
                name = person[0]

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return

        frame = jpeg.tobytes()

        if name != UNKNOWN:
            alert(name, frame)
        
        return frame
