from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
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
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()

    #room_messages = Message.objects.filter(Q(room__topic__name=q))#consigue los mensajes que contengan q en el nombre, topico o descripcion
    if (request.user.is_authenticated):
        if (q == ''):
            room_messages = Message.objects.filter(Q(room__participants__in=[request.user]))
        else:
            room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) & Q(room__participants__in=[request.user]))
    else:
        if (q == ''):
            room_messages = Message.objects.all()
        else:
            room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    return render(request, 'baseline/home.html', {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages': room_messages})

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()#consigue todos los mensajes del room y los ordena por fecha
    #notacion: room.message_set.all() es lo mismo que Message.objects.filter(room=room)

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)#agrega el usuario a la lista de participantes del room
        return redirect('room', pk=room.id)




    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': room.participants.all()
    }
    return render(request, 'baseline/room.html', context)

@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),#'name' es el name del input en el html
            description=request.POST.get('description')
        )
        return redirect('/')

    context = {'form': form, 'topics': Topic.objects.all()}
    return render(request, 'baseline/room_form.html', context)

@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)#consigue el Room por id
    form = RoomForm(instance=room)#hace que los valores default del form coincidan con los del Room

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)


        #form = RoomForm(request.POST, instance=room)#mete el json en un objeto RoomForm, el instance=room para que actualize en vez de postear un new
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('room', pk=room.id)

    context = {'form': form, 'topics': Topic.objects.all(), 'room': room}
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
        username = request.POST.get('username').lower()
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

    context = {'page': 'login'}
    return render(request, 'baseline/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('/')

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)#mete el json en un objeto RoomForm
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.username = form.cleaned_data.get('username')
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error has ocurred during registration')

    context = {'page': 'register', 'form': form}
    return render(request, 'baseline/login_register.html', context)

@login_required(login_url='loginPage')
def deleteMsg(request, pk):
    msg = Message.objects.get(id=pk)

    #comment = request.POST.get('comment')

    if request.user != msg.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        msg.delete()
        return redirect('/')

    return render(request, 'baseline/delete.html', {'obj': msg})

def userProfile(req, pk):
    user = User.objects.get(id=pk)

    rooms = user.participants.all()

    room_messages = user.message_set.all()

    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }
    return render(req, 'baseline/profile.html', context)

@login_required(login_url='loginPage')
def updateUser(req):
    user = req.user
    form = UserForm(instance=user)

    if req.method == 'POST':
        form = UserForm(req.POST, req.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        'form': form
    }
    return render(req, 'baseline/update-user.html', context)

def topicsPage(req):
    topics = Topic.objects.all()

    q = req.GET.get('q')#consigue el valor de q en el url
    if (not q):
        q = ''

    topics = Topic.objects.filter(name__icontains=q)#consigue los topics que contengan q en el nombre



    context = {
        'topics': topics
    }
    return render(req, 'baseline/topics.html', context)

def activityPage(req):
    room_messages = Message.objects.all()
    context = {
        'room_messages': room_messages
    }
    return render(req, 'baseline/activity.html', context)