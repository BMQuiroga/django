from rest_framework.serializers import ModelSerializer
from baseline.models import Room, User, Message

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'avatar', 'bio']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'