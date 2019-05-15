from channels.generic.websocket import WebsocketConsumer
import json
from .utils import detections_watcher


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        detections_watcher.subscribe(self.notify_detection)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def notify_detection(self, person_name, city_name, detection_url):
        self.send(text_data=json.dumps({
            'person_name': person_name,
            'city_name': city_name,
            'detection_url': detection_url,
        }))