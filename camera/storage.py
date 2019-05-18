import os
import pickle


_classifier_dir = os.path.abspath('./classifier/')
_classifier_path = os.path.join(_classifier_dir, 'classifier.clf')
_classifier_date_path = os.path.join(_classifier_dir, 'date.pkl')
_settings_path = os.path.join(_classifier_dir, 'settings.pkl')
_settings_date_path = os.path.join(_classifier_dir, 'settings_date.pkl') 


def _load_pickle(path):
    if not os.path.isfile(path):
        return

    with open(path, 'rb') as f:
        return pickle.load(f)


def _dump_pickle(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def create__classifier_dir():
    if not os.path.isdir(_classifier_dir):
        os.mkdir(_classifier_dir)


def save_classifier_date(date):
    create__classifier_dir()
    _dump_pickle(_classifier_date_path, date)


def save_classifier(classifier):
    create__classifier_dir()

    with open(_classifier_path, 'wb') as f:
        f.write(classifier)


def save_settings_date(date):
    create__classifier_dir()
    _dump_pickle(_settings_date_path, date)


def save_settings(settings):
    create__classifier_dir()
    _dump_pickle(_settings_path, settings)


def get_classifier_date():
    return _load_pickle(_classifier_date_path)

    
def get_classifier():
    return _load_pickle(_classifier_path)


def get_settings_date():
    return _load_pickle(_settings_date_path)


def get_settings():
    return _load_pickle(_settings_path)