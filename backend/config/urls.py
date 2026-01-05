
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Plantacion.url')),
    path('api/', include('Alerta.urls')),
    path('api/', include('users.urls')),
]
