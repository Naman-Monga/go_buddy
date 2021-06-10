from django.urls import path
from .views import room, create_room
urlpatterns = [
    path('room/<str:room_name>', room, name="room"),
    path('create-room/', create_room, name='createroom')
]
