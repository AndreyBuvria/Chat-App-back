from django.urls import re_path
from channels.routing import URLRouter

from chatroom.consumers import ChatConsumer

websocket_urlpatterns = URLRouter([
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
])