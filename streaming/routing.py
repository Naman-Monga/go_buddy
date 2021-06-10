from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/stream/(?P<room_name>\w+)/$', consumers.StreamRoomConsumer.as_asgi())
] 