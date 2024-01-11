from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('baseline.urls')),
    path('api/', include('baseline.api.urls')),
]
