from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server-stat/', consumer.StatConsumer.as_asgi())
]