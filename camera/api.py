import urllib.request
from datetime import datetime
import requests
from threading import Thread


_camera_name = 'camera4'
_camera_city = 'Pernik'
_base_url = 'http://localhost:8000/rest/'
_classifier_url = f'{_base_url}classifier'
_classifier_date_url = f'{_base_url}classifier/date'
_camera_register_url = f'{_base_url}cameras'
_add_detection_url = f'{_base_url}detections'
_settings_url = f'{_base_url}settings'
_settings_date_url = f'{_settings_url}/date'
_alerts = {}
_settings_date = None
_classifier_date = None
_settings = None
_classifier = None


def get_settings():
    return _settings


def get_classifier():
    return _classifier


def alert(name, frame):
    def alert_request():
        data = { 'name': name, 'city': _camera_city }
        requests.post(url=_add_detection_url, data=data, files={ 'image': ('image.jpg', frame) })

    should_alert = False

    if not _alerts.get(name):
        _alerts[name] = datetime.utcnow()
        should_alert = True
    else:
        now = datetime.utcnow()
        last_alerted = _alerts[name]
        diff = now - last_alerted
        
        if diff.seconds / 60 > _settings['alert_timeout']:
            _alerts[name] = now
            should_alert = True
        
    if should_alert:
        Thread(target=alert_request).start()


def register_camera():
    data = { 'city': _camera_city, 'name': _camera_name, 'url': 'http://localhost:5000/feed' }
    requests.post(url=_camera_register_url, json=data)


def download_settings():
    print('pulled new settings')

    return requests.get(url=_settings_url).json()


def download_settings_date():
    return requests.get(url=_settings_date_url).json()['date']


def download_classifier():
    print('pulled new classifier')
    
    return urllib.request.urlopen(_classifier_url).read()


def download_classifier_date():
    return requests.get(url=_classifier_date_url).json()['date']


def update():
    global _classifier
    global _classifier_date
    global _settings
    global _settings_date

    remote_classifier_date = download_classifier_date()
    remote_classifier = download_classifier()
    remote_settings_date = download_settings_date()
    remote_settings = download_settings()

    if not _classifier_date or not _classifier or \
        _classifier_date != remote_classifier_date:
        _classifier = remote_classifier
        _classifier_date = remote_classifier_date

    if not _settings_date or not _settings or \
        _settings_date != remote_settings_date:
        _settings = remote_settings
        _settings_date = remote_classifier_date