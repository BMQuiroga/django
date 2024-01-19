from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from baseline.models import Room, User, Message
from .serializers import RoomSerializer, UserSerializer, MessageSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/rooms/:id/messages',
        'GET /api/users',
        'GET /api/users/:id',

    ]
    return Response(routes)#permite que las rutas usen data json en vez de diccionarios de py

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    #no puede mandar una lista de python, se usan serializers
    serializer = RoomSerializer(rooms, many=True)# many es para que sepa que es una lista (muchos objetos)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    #no puede mandar una lista de python, se usan serializers
    serializer = RoomSerializer(room, many=False)# many es para que sepa que es una lista (muchos objetos)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request, pk):
    messages = Room.objects.get(id=pk).message_set.all()

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

