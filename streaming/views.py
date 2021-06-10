from django.shortcuts import render, redirect
from .models import Room
# Create your views here.


def room(request, room_name):
    curr_room = Room.objects.filter(room_name=room_name)[0]
    iamadmin = 0
    if(curr_room.admin==request.user.id):
        iamadmin=1
    context = {'room_name':room_name, 'admin':curr_room.admin,'iamadmin':iamadmin}
    return render(request, 'streaming/index.html', context)

def create_room(request):

    if request.method=="POST":
        room_name = request.POST.get('roomName')
        if room_name=="":
            return render(request, 'streaming/createRoom.html')
        myroom = Room( admin=request.user.id, room_name=room_name)
        myroom.save()
        return redirect('room', room_name=room_name)

    return render(request, 'streaming/createRoom.html')