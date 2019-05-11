import urllib.request
import threading
from time import sleep
from django.db import transaction
from ..models import Camera


def delete_camera(camera):
    with transaction.atomic():
        camera.delete()


def check_cameras():
    while True:
        cameras = Camera.objects.select_for_update().all()

        for camera in cameras:
            try:
                code = urllib.request.urlopen(camera.url).getcode()

                if code != 200:
                    delete_camera(camera)
            except:
                delete_camera(camera)
        
        sleep(180)


def start_watcher_thread():
    thread = threading.Thread(target=check_cameras)
    thread.start()