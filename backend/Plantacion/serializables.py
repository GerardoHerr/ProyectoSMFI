from rest_framework import serializers
from .models import Plantacion, Cultivo, Sensor, ConfiguracionUmbral

class PlantacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantacion
        fields = ('id', 'nombre', 'fechaRegistro', 'espacio', 'cultivo', 'sensores', 'usuario')

class CultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivo
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class ConfiguracionUmbralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionUmbral
        fields = '__all__'