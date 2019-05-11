"""
WSGI config for watcher_camera project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from server.ai.trainer import start_training_thread
from server.utils.cameras_watcher import start_watcher_thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watcher_server.settings')

application = get_wsgi_application()

start_training_thread()
start_watcher_thread()