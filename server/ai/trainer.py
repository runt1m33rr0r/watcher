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
from ..models import ClassifierCreationDate, Settings
from ..utils.storage import PERSONS_FOLDER_NAME


train_timeout = 180


def resize_image(image):
    converted = Image.fromarray(image)
    size = 1024, 1024

    if converted.size[0] > size[0] or converted.size[1] > size[0]:
        converted.thumbnail(size, Image.ANTIALIAS)

    return numpy.array(converted)


def train(train_path):
    if not os.path.isdir(train_path):
        return

    X = []
    y = []

    for class_path in os.listdir(train_path):
        if not os.path.isdir(os.path.join(train_path, class_path)):
            continue

        for img_path in image_files_in_folder(os.path.join(train_path, class_path)):
            image = face_recognition.load_image_file(img_path)
            # image = resize_image(image)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) == 0:
                print("No face in {}.".format(img_path))
            elif len(face_bounding_boxes) > 1:
                print("More than on face in {}.".format(img_path))
            else:
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_path)

    if len(X) == 0 or len(y) == 0:
        return

    n_neighbors = int(round(math.sqrt(len(X))))
    print("Chose n_neighbors automatically:", n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X, y)

    return knn_clf


folder_modified = True


class FileEvent(LoggingEventHandler):
    def dispatch(self, event):
        global folder_modified
        folder_modified = True


def save_date():
    ClassifierCreationDate.objects.update_or_create()


def training_thread():
    global folder_modified

    event_handler = FileEvent()
    observer = Observer()
    path = os.path.abspath(f'./media/{PERSONS_FOLDER_NAME}')

    if not os.path.isdir(path):
        os.makedirs(path)

    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    while True:
        if folder_modified:
            print('training')
            classifier = train(os.path.abspath(path))
            
            save_classifier(classifier)
            save_date()
            
            folder_modified = False
        
        sleep(180)


def start_training_thread():
    train_timeout = Settings.objects.get_or_create()[0].model_training_timeout * 60
    thread = threading.Thread(target=training_thread)
    thread.start()

    print('thread started')