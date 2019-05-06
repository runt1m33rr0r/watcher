import math
from sklearn import neighbors
import os
import os.path
from PIL import Image
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy
import cv2
import threading
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from time import sleep
from .classifier import save_classifier
from .classifier import classifier_path
from ..models import ClassifierCreationDate
from ..utils.storage import PERSONS_FOLDER_NAME


def resize_image(image):
    converted = Image.fromarray(image)
    size = 1024, 1024

    if converted.size[0] > size[0] or converted.size[1] > size[0]:
        converted.thumbnail(size, Image.ANTIALIAS)

    return numpy.array(converted)


def train(train_dir):
    X = []
    y = []

    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            image = resize_image(image)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) == 0:
                print("No face in {}.".format(img_path))
            elif len(face_bounding_boxes) > 1:
                print("More than on face in {}.".format(img_path))
            else:
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    n_neighbors = int(round(math.sqrt(len(X))))
    print("Chose n_neighbors automatically:", n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X, y)

    return knn_clf


def predict(image, knn_clf, distance_threshold=0.6):
    face_locations = face_recognition.face_locations(image, model='cnn')

    if len(face_locations) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), face_locations, are_matches)]


folder_modified = True


class FileEvent(LoggingEventHandler):
    def dispatch(self, event):
        global folder_modified
        folder_modified = True


def save_date():
    date = None
    if ClassifierCreationDate.objects.filter().exists():
        date = ClassifierCreationDate.objects.get()
    else:
        date = ClassifierCreationDate()
    date.save()


def training_thread():
    global folder_modified

    event_handler = FileEvent()
    observer = Observer()
    path = os.path.abspath(f'./media/{PERSONS_FOLDER_NAME}')
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    while True:
        if folder_modified:
            print('training')
            classifier = train(os.path.abspath(f'./media/{PERSONS_FOLDER_NAME}'))
            
            save_classifier(classifier)
            save_date()
            
            folder_modified = False
        
        sleep(180)


def start_training_thread():
    thread = threading.Thread(target=training_thread)
    thread.start()

    print('thread started')