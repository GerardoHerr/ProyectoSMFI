from django.db import models
from django.utils import timezone
from Plantacion.models import Plantacion

class Accion(models.Model):
    tipoAccion = models.CharField(max_length=100)
    fechaEjecucion = models.DateField(default=timezone.now)

    def ejecutarAccion(self):
        pass

    def __str__(self):
        return self.tipoAccion

class Recomendacion(models.Model):
    descripcion = models.CharField(max_length=200)
    fechaEmision = models.DateField(default=timezone.now)

    def __str__(self):
        return self.descripcion

class Alerta(models.Model):  

    ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('atendida', 'Atendida'),
    ('ejecutada', 'Ejecutada'),
    ]

    TIPOS_ALERTA = [
        ('riego', 'Riego'),
        ('secado', 'Secado'),
    ]

    plantacion = models.ForeignKey(Plantacion, on_delete=models.CASCADE, related_name="alertas")
    tipoAlerta = models.CharField(
        max_length=50,
        choices=TIPOS_ALERTA
    )
    descripcion = models.CharField(max_length=200)
    fechaGeneracion = models.DateTimeField(
        default=timezone.now
    )
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    accion = models.ForeignKey(Accion, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas')
    recomendacion = models.ForeignKey(
        Recomendacion,
        on_delete=models.CASCADE,
        related_name='alertas'
    )

    def __str__(self):
        return self.tipoAlerta



