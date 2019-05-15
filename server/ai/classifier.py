import pickle
import os
import cv2
import face_recognition
import numpy as np
from config_app.settings import BASE_DIR
import pickle
from PIL import Image
from ..models import Settings
import sys
from common.ai import predict, draw_boxes


UNKNOWN = 'unknown'
classifier_dir = os.path.join(BASE_DIR, 'classifier')
classifier_path = f'{classifier_dir}/knn_model.clf'


def save_classifier(classifier):
    if not os.path.isdir(classifier_dir):
        os.mkdir(classifier_dir)

    with open(classifier_path, 'wb') as f:
        pickle.dump(classifier, f)

    print('saved classifier')


def get_classifier():
    if os.path.exists(classifier_path):
        with open(classifier_path, 'rb') as f:
            return pickle.load(f)
    else:
        return None


class ImageProcessor(object):
    _settings = None
    _downscale = None
    _sensitivity = None
    _classifier = None
    _initialized = False

    @classmethod
    def _init(cls):
        if cls._initialized:
            return

        cls._settings = Settings.objects.get_or_create()[0]
        cls._downscale = cls._settings.downscale_level
        cls._sensitivity = cls._settings.detection_sensitivity
        cls._classifier = get_classifier()
        cls._initialized = True

    @classmethod
    def process_frame(cls, frame):
        cls._init()

        frame = Image.open(frame)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        prediction = predict(frame, cls._classifier, cls._downscale, cls._sensitivity)
        draw_boxes(frame, prediction, cls._downscale)

        ret, jpeg = cv2.imencode('.jpg', frame)

        if not ret:
            return

        return jpeg.tobytes()
