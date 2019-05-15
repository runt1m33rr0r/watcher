import cv2
import face_recognition


_UNKNOWN = 'unknown'


def draw_boxes(frame, prediction, downscale):
    for name, (top, right, bottom, left) in prediction:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= downscale
        right *= downscale
        bottom *= downscale
        left *= downscale

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    
def predict(image, classifier, downscale, sensitivity):
        if not classifier:
            return []

        scale = 1.0 / downscale
        image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        converted_frame = image[:, :, ::-1]
        face_locations = face_recognition.face_locations(image, model='cnn')

        if len(face_locations) == 0:
            return []
        
        faces_encodings = face_recognition.face_encodings(image, face_locations)
        distance_threshold = sensitivity
        closest_distances = classifier.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

        return [(pred, loc) if rec else (_UNKNOWN, loc) for pred, loc, rec in zip(classifier.predict(faces_encodings), face_locations, are_matches)]