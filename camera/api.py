import urllib.request
from datetime import datetime
import requests
from threading import Thread
import pickle


CONNECTION_ERROR = 'COULD NOT CONNECT TO MAIN SERVER!!!'

_camera_name = 'camera'
_camera_city = 'City'
_camera_host = '0.0.0.0'
_camera_port = 5000
_camera_url = f'http://{_camera_host}:{_camera_port}/feed'
_central_server = 'http://localhost:8000/'
_base_url = f'{_central_server}rest/'
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


def _set_camera_url(host, port):
    global _camera_url, _camera_port, _camera_host
    _camera_host = host
    _camera_port = port
    _camera_url = f'http://{_camera_host}:{_camera_port}/feed'


def _register_camera():
    try:
        data = { 'city': _camera_city, 'name': _camera_name, 'url': _camera_url }
        requests.post(url=_camera_register_url, json=data)
    except:
        print(CONNECTION_ERROR)


def get_settings():
    return _settings


def get_classifier():
    return _classifier


def set_camera_name(name):
    global _camera_name
    _camera_name = name


def set_camera_city(city_name):
    global _camera_city
    _camera_city = city_name


def set_camera_host(host):
    _set_camera_url(host, _camera_port)


def set_camera_port(port):
    _set_camera_url(_camera_host, port)


def set_central_server(server):
    global _central_server
    _central_server = server


def alert(name, frame):
    def alert_request():
        try:
            data = { 'name': name, 'city': _camera_city }
            requests.post(url=_add_detection_url, data=data, files={ 'image': ('image.jpg', frame) })
        except:
            print(CONNECTION_ERROR)

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


def download_settings():
    try:
        res = requests.get(url=_settings_url).json()
        print('pulled new settings')

        return res
    except:
        print(CONNECTION_ERROR)

    return None


def download_settings_date():
    try:
        res = requests.get(url=_settings_date_url).json()['date']

        return res
    except:
        print(CONNECTION_ERROR)

    return None


def download_classifier():
    try:
        res = urllib.request.urlopen(_classifier_url).read()
        print('pulled new classifier')

        return pickle.loads(res)
    except Exception as e:
        print(e)
        print(CONNECTION_ERROR)
    
    return None


def download_classifier_date():
    try:
        res = requests.get(url=_classifier_date_url).json()['date']

        return res
    except:
        print(CONNECTION_ERROR)
        
    return None


def update():
    _register_camera()

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