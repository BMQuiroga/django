from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
'''
rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'This is a room for COVID-19 patients'},
    {'id': 2, 'name': 'Room 2', 'description': 'This is a room for patients with other illnesses'},
    {'id': 3, 'name': 'Room 3', 'description': 'This is a room for kids'},

]'''



def home(request):
    

    q = request.GET.get('q')#consigue el valor de q en el url
    if (not q):
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )#consigue los rooms que contengan q en el nombre, topico o descripcion
    topics = Topic.objects.all()
    rooms_count = rooms.count()



    return render(request, 'baseline/home.html', {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count})

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    context = {
        'room': room
    }
    return render(request, 'baseline/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        #print(request.POST)
        form = RoomForm(request.POST)#mete el json en un objeto RoomForm
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'baseline/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)#consigue el Room por id
    form = RoomForm(instance=room)#hace que los valores default del form coincidan con los del Room

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)#mete el json en un objeto RoomForm, el instance=room para que actualize en vez de postear un new
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'baseline/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')

    #context = {'item': room}
    #return render(request, 'baseline/room_.html', context)
    return render(request, 'baseline/delete.html', {'obj': room})