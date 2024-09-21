from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Room, Messages

@login_required(login_url='/login')
def rooms(request):
    Rooms = Room.objects.all()

    return render(request,'room/rooms.html',{'rooms' : Rooms})

@login_required(login_url='/login')
def room(request,slug):
    room = Room.objects.get(slug=slug)
    message = Messages.objects.filter(room=room)

    return render(request,'room/room.html',{'room' : room,'messages':message})
