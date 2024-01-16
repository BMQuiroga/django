from django.forms import ModelForm
from .models import Room, Topic, Message, User
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','avatar','bio']
        #fields = ['username']

