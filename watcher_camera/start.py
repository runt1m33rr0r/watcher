import face_recognition
import cv2
import time
import math
from sklearn import neighbors
import pickle
import os
import os.path
from face_recognition.face_recognition_cli import image_files_in_folder


def draw_box(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 1
        right *= 1
        bottom *= 1
        left *= 1

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


def detect():
    video_capture = cv2.VideoCapture(0)
    classifier = train("images")

    # image = face_recognition.load_image_file("images/ciri1.jpg")
    # encoding = face_recognition.face_encodings(image)

    face_locations = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        converted_frame = frame[:, :, ::-1]

        if process_this_frame:
            face_names = []

            prediction = predict(converted_frame, classifier)
            print(prediction)

            # face_locations = face_recognition.face_locations(converted_frame, model="cnn")
            # face_encodings = face_recognition.face_encodings(converted_frame, face_locations)

            # for face_encoding in face_encodings:
            #     matches = face_recognition.compare_faces(encoding, face_encoding)

            #     if True in matches:
            #         face_names.append("ciri")
            #     else:
            #         face_names.append("unknown")
            
        process_this_frame = not process_this_frame

        draw_box(frame, face_locations, face_names)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()


def train(train_dir):
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    n_neighbors = int(round(math.sqrt(len(X))))
    print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm="ball_tree", weights="distance")
    knn_clf.fit(X, y)

    return knn_clf


def predict(image, knn_clf):
    face_locations = face_recognition.face_locations(image, model="cnn")

    if len(face_locations) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

    # Use the KNN model to find the best matches for the test face
    distance_threshold = 0.6
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), face_locations, are_matches)]


if __name__ == "__main__":
    detect()
