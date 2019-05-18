import urllib.request
from datetime import datetime
import requests
from threading import Thread
from .storage import *


camera_name = 'camera4'
camera_city = 'Pernik'
base_url = 'http://localhost:8000/rest/'
classifier_url = f'{base_url}classifier'
classifier_date = f'{base_url}classifier/date'
camera_register_url = f'{base_url}cameras'
add_detection_url = f'{base_url}detections'
settings_url = f'{base_url}settings'
settings_date = f'{settings_url}/date'


alerts = {}
settings = {
    'detection_sensitivity': 0.55,
    'downscale_level': 2,
    'alert_timeout': 3,
    'camera_update_timeout': 3,
}


def alert(name, frame):
    def alert_request():
        data = { 'name': name, 'city': camera_city }
        requests.post(url=add_detection_url, data=data, files={ 'image': ('image.jpg', frame) })

    should_alert = False

    if not alerts.get(name):
        alerts[name] = datetime.utcnow()
        should_alert = True
    else:
        now = datetime.utcnow()
        last_alerted = alerts[name]
        diff = now - last_alerted
        
        if diff.seconds / 60 > settings['alert_timeout']:
            alerts[name] = now
            should_alert = True
        
    if should_alert:
        Thread(target=alert_request).start()


def register_camera():
    data = { 'city': camera_city, 'name': camera_name, 'url': 'http://localhost:5000/feed' }
    requests.post(url=camera_register_url, json=data)


def download_settings():
    return requests.get(url=settings_url).json()


def download_settings_date():
    data = requests.get(url=settings_date).json()

    return data['date']


def download_classifier():
    print('pulled new classifier')
    response = urllib.request.urlopen(classifier_url)

    return response.read()


def download_classifier_date():
    data = requests.get(url=classifier_date).json()

    return data['date']


def update():
    local_classifier_date = get_classifier_date()
    local_classifier = get_classifier()
    remote_classifier_date = download_classifier_date()
    remote_classifier = download_classifier()

    local_settings_date = get_settings_date()
    local_settings = get_settings()
    remote_settings_date = download_settings_date()
    remote_settings = download_settings()

    if (not local_classifier_date or not local_classifier) or \
        local_classifier_date != remote_classifier_date:
        save_classifier(remote_classifier)
        save_classifier_date(remote_classifier_date)

    if (not local_settings_date or not local_settings) or \
        local_settings_date != remote_settings_date:
        save_settings(remote_settings)
        save_settings_date(remote_settings_date)

    settings = get_settings()
