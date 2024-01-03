from django.shortcuts import render
from .models import Room
'''
rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'This is a room for COVID-19 patients'},
    {'id': 2, 'name': 'Room 2', 'description': 'This is a room for patients with other illnesses'},
    {'id': 3, 'name': 'Room 3', 'description': 'This is a room for kids'},

]'''



def home(request):
    rooms = Room.objects.all()
    return render(request, 'baseline/home.html', {'rooms': rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {
        'room': room
    }
    return render(request, 'baseline/room.html', context)



# Create your views here.
