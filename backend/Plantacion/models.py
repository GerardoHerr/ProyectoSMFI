from django.db import models
from django.utils import timezone

class VariableAmbiental(models.Model):
    nombre = models.CharField(max_length=100)
    unidad = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class ConfiguracionUmbral(models.Model):
    valorMinimo = models.FloatField()
    valorMaximo = models.FloatField()
    fechaConfiguracion = models.DateField(default=timezone.now)
    variableAmbiental  = models.ForeignKey(VariableAmbiental, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.valorMinimo} - {self.valorMaximo}"


class Cultivo(models.Model):
    nombreCultivo = models.CharField(max_length=100)
    tipoCultivo = models.CharField(max_length=100)
    familia = models.CharField(max_length=100)
    semilla = models.CharField(max_length=100)
    configuracion = models.ForeignKey(
        ConfiguracionUmbral, on_delete=models.CASCADE, related_name="cultivos"
    )

    def __str__(self):
        return self.nombreCultivo

class DatoSensor(models.Model):
    valor = models.FloatField()
    fechaRegistro = models.DateField(default=timezone.now)
    horaRegistro = models.TimeField(default=timezone.now)
    variableAmbiental = models.ForeignKey(VariableAmbiental, on_delete=models.CASCADE)

    def obtener_valor(self):
        return self.valor

    def __str__(self):
        return f"{self.sensor.tipoSensor}: {self.valor}"

class Sensor(models.Model):
    tipoSensor = models.CharField(max_length=100)
    estado = models.CharField(max_length=30)
    ubicacion = models.CharField(max_length=100)
    datoSensor = models.ManyToManyField(DatoSensor, related_name="sensores", blank=True)

    def __str__(self):
        return self.tipoSensor

class ConfiguracionTomaDecision(models.Model):
    tipoConfiguracion = models.CharField(max_length=100)
    criterioDecision = models.CharField(max_length=100)
    fechaConfiguracion = models.DateField()

class Plantacion(models.Model):
    nombre = models.CharField(max_length=100)
    fechaRegistro = models.DateField(default=timezone.now)
    espacio = models.FloatField()
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    sensores = models.ManyToManyField(Sensor, related_name="plantaciones")
    usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='plantaciones')
    configuracionTomaDecision = models.ForeignKey(ConfiguracionTomaDecision, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def excede_valor_umbral(self, dato: DatoSensor):
        return None

    def generar_alerta(self, dato: DatoSensor):
        return None

#comentario