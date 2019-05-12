import cv2
from PIL import Image
from io import BytesIO
from api import alert, get_classifier, update_classifier
import face_recognition
from time import sleep
import threading


UNKNOWN = 'unknown'


class ImageProcessor(object):
    _can_process = True
    _classifier = None
    _updater_thread = None

    @staticmethod
    def initialize():
        if not ImageProcessor._updater_thread:
            ImageProcessor._updater_thread = threading.Thread(target=ImageProcessor._classifier_updater_thread)
            ImageProcessor._updater_thread.start()

    @staticmethod
    def _classifier_updater_thread():
        while True:
            print('updating classifier')

            ImageProcessor._can_process = False
            update_classifier()
            ImageProcessor._classifier = get_classifier()
            ImageProcessor._can_process = True

            sleep(300)

    @staticmethod
    def _draw_boxes(frame, prediction):
        for name, (top, right, bottom, left) in prediction:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    @staticmethod
    def _predict(image):
        if not ImageProcessor._classifier:
            return []

        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        converted_frame = image[:, :, ::-1]
        face_locations = face_recognition.face_locations(image, model='cnn')

        if len(face_locations) == 0:
            return []
        
        faces_encodings = face_recognition.face_encodings(image, face_locations)
        distance_threshold = 0.55
        closest_distances =  ImageProcessor._classifier.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

        return [(pred, loc) if rec else (UNKNOWN, loc) for pred, loc, rec in zip(ImageProcessor._classifier.predict(faces_encodings), face_locations, are_matches)]

    @staticmethod
    def process_video_frame(frame):
        if ImageProcessor._can_process:
            prediction = ImageProcessor._predict(frame)
            ImageProcessor._draw_boxes(frame, prediction)

            for person in prediction:
                name = person[0]

                if name != UNKNOWN:
                    alert(name, frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return

        frame = jpeg.tobytes()
        return frame
