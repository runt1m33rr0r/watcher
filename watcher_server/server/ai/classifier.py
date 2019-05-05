import pickle
import os
from watcher_server.settings import BASE_DIR


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
        with open(classifier_path, 'r') as f:
            file_data = f.read()
            return file_data
    else:
        return None
