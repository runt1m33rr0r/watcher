import urllib.request
import os
import requests
import pickle
from datetime import datetime


camera_name = 'camera4'
camera_city = 'Pernik'
base_url = 'http://localhost:8000/'
classifier_url = f'{base_url}classifier'
camera_register_url = f'{base_url}cameras/register'
add_detection_url = f'{base_url}detections'

classifier_date = f'{base_url}classifier/date'
classifier_dir = os.path.abspath('./classifier/')
classifier_path = os.path.join(classifier_dir, 'classifier.clf')
classifier_date_path = os.path.join(classifier_dir, 'date.pkl')
alert_timeout_minutes = 3
alerts = {}


def alert(name, frame):
    should_alert = False

    if not alerts.get(name):
        alerts[name] = datetime.utcnow()
        should_alert = True
    else:
        now = datetime.utcnow()
        last_alerted = alerts[name]
        diff = now - last_alerted
        
        if diff.seconds / 60 > alert_timeout_minutes:
            alerts[name] = now
            should_alert = True
        
    if should_alert:
        data = { 'name': name, 'camera_name': camera_name, 'city': camera_city }
        requests.post(url=add_detection_url, data=data, files={'image': ('image.jpg', frame)})


def register_camera():
    data = { 'city': camera_city, 'name': camera_name, 'url': 'http://localhost:5000/feed' }
    requests.post(url=camera_register_url, json=data)


def create_classifier_dir():
    if not os.path.isdir(classifier_dir):
        os.mkdir(classifier_dir)


def download_classifier():
    print('pulled new classifier')
    
    create_classifier_dir()

    response = urllib.request.urlopen(classifier_url)
    return response.read()


def download_classifier_date():
    create_classifier_dir()

    resp = requests.get(url=classifier_date)
    data = resp.json()

    return data['date']


def _deserialize_pickle(path):
    if not os.path.isfile(path):
        return None

    with open(path, 'rb') as f:
        return pickle.load(f)


def save_classifier_date(date):
    create_classifier_dir()
    
    with open(classifier_date_path, 'wb') as f:
        pickle.dump(date, f)


def save_classifier(classifier):
    create_classifier_dir()

    with open(classifier_path, 'wb') as f:  
        f.write(classifier)


def get_classifier_date():
    return _deserialize_pickle(classifier_date_path)

    
def get_classifier():
    return _deserialize_pickle(classifier_path)


def update_classifier():
    local_classifier_date = get_classifier_date()
    local_classifier = get_classifier()
    remote_classifier_date = download_classifier_date()
    remote_classifier = download_classifier()

    if (not local_classifier_date or not local_classifier) or \
        (local_classifier_date != remote_classifier_date):
        save_classifier(remote_classifier)
        save_classifier_date(remote_classifier_date)
