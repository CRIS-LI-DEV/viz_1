from django.urls import re_path
from app.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sala>\w+)/$', ChatConsumer.as_asgi()),
]
