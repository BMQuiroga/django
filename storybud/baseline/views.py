from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'This is a room for COVID-19 patients'},
    {'id': 2, 'name': 'Room 2', 'description': 'This is a room for patients with other illnesses'},
    {'id': 3, 'name': 'Room 3', 'description': 'This is a room for kids'},

]



def home(request):
    return render(request, 'baseline/home.html', {'rooms': rooms})

def room(request, pk=None):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
            break

    context = {
        'room': room
    }
    return render(request, 'baseline/room.html', context)



# Create your views here.
