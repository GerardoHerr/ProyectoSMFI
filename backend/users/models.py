from django.db import models
from django.utils import timezone

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    isActivo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    isActivo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
