from django.shortcuts import render, redirect
from .models import Room
import uuid 
# Create your views here.


def room(request, room_name):
    curr_room = Room.objects.filter(room_name=room_name)[0]
    iamadmin = 0
    if(curr_room.admin==request.user.id):
        iamadmin=1
    context = {'room_name':room_name, 'admin':curr_room.admin,'iamadmin':iamadmin, 'room_title':curr_room.room_title}
    return render(request, 'streaming/index.html', context)

def create_room(request):

    if request.method=="POST":
        room_title = request.POST.get('roomName')
        room_name = uuid.uuid4().hex[:10] # Creates a random id of 10 characters.
        myroom = Room( admin=request.user.id, room_name=room_name, room_title=room_title)
        myroom.save()
        return redirect('room', room_name=room_name)

    return render(request, 'streaming/createRoom.html')