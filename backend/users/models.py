from django.db import models
from django.utils import timezone

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    isActivo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    clave = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
