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
classifier_path = f'{classifier_dir}/classifier.clf'

_settings = None
_downscale = None
_sensitivity = None
_classifier = None
_initialized = False


def _init():
    global _initialized

    if _initialized:
        return

    global _settings
    global _downscale
    global _sensitivity
    global _classifier

    _settings = Settings.objects.get_or_create()[0]
    _downscale = _settings.downscale_level
    _sensitivity = _settings.detection_sensitivity
    _classifier = get_classifier()
    _initialized = True


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


def process_frame(frame):
    _init()

    frame = Image.open(frame)
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    prediction = predict(frame, _classifier, _downscale, _sensitivity)
    draw_boxes(frame, prediction, _downscale)

    ret, jpeg = cv2.imencode('.jpg', frame)

    if not ret:
        return

    return jpeg.tobytes()
