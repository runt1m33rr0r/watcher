import cv2
from PIL import Image
from io import BytesIO
from api import alert, get_classifier
import face_recognition


UNKNOWN = 'unknown'


class ImageProcessor(object):
    def __init__(self):
        self.classifier = get_classifier()

    def draw_boxes(self, frame, prediction):
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

    def predict(self, image):
        if not self.classifier:
            return []

        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        converted_frame = image[:, :, ::-1]
        face_locations = face_recognition.face_locations(image, model='cnn')

        if len(face_locations) == 0:
            return []
        
        faces_encodings = face_recognition.face_encodings(image, face_locations)
        distance_threshold = 0.55
        closest_distances = self.classifier.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

        return [(pred, loc) if rec else (UNKNOWN, loc) for pred, loc, rec in zip(self.classifier.predict(faces_encodings), face_locations, are_matches)]

    def process_video_frame(self, frame):
        prediction = self.predict(frame)
        self.draw_boxes(frame, prediction)

        ret, jpeg = cv2.imencode('.jpg', frame)

        if not ret:
            return

        frame = jpeg.tobytes()

        for person in prediction:
            name = person[0]

            if name != UNKNOWN:
                alert(name, frame)

        return frame
