from django.shortcuts import render
from .serializables import AlertaSerializer
from .models import Alerta
from rest_framework import viewsets

# Create your views here.
class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

