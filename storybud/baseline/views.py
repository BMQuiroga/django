from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

@login_required(login_url='loginPage')
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

@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)#consigue el Room por id
    form = RoomForm(instance=room)#hace que los valores default del form coincidan con los del Room

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)#mete el json en un objeto RoomForm, el instance=room para que actualize en vez de postear un new
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'baseline/room_form.html', context)

@login_required(login_url='loginPage')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('/')

    #context = {'item': room}
    #return render(request, 'baseline/room_.html', context)
    return render(request, 'baseline/delete.html', {'obj': room})

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #user = authenticate(request, username=username, password=password)
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'baseline/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')