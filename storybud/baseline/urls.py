from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('delete-msg/<str:pk>/', views.deleteMsg, name='delete-msg'),

    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    path('update-user/', views.updateUser, name='update-user'),
]