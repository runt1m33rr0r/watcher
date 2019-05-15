from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from .ai.trainer import start_training_thread
from .utils.cameras_watcher import start_watcher_thread
from .consumers import *


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url('notifications', NotificationConsumer),
        ])
    ),
})

start_training_thread()
start_watcher_thread()