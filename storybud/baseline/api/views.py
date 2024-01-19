from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from baseline.models import Room, User, Message
from .serializers import RoomSerializer, UserSerializer, MessageSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

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

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])  # Use the authentication classes you need
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def publishMessage(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {'body': request.data.get('body'), 'user': request.user.pk, 'room': room.pk}

    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)