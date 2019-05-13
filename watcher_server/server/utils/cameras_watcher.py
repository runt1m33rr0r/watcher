import urllib.request
import threading
from time import sleep
from django.db import transaction
from ..models import Camera, Settings


check_interval = 180


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
        
        sleep(check_interval)


def start_watcher_thread():
    check_interval = Settings.objects.get_or_create()[0].camera_check_timeout * 60
    thread = threading.Thread(target=check_cameras)
    thread.start()