from datetime import timedelta
import random
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Plantacion, Cultivo, Sensor, ConfiguracionUmbral
from .serializables import PlantacionSerializer, CultivoSerializer, SensorSerializer, ConfiguracionUmbralSerializer
from django.utils import timezone

# Create your views here.
class plantacionViewSet(ModelViewSet):
    serializer_class = PlantacionSerializer
    queryset = Plantacion.objects.all()

class PlantacionSensoresView(APIView): 
    def get(self, request, plantacion_id, ultimoValor):
        try:
            plantacion = Plantacion.objects.get(id=plantacion_id)
            sensor_data = []
            for sensor in plantacion.sensores.all():
                datoSimulado = []
                now = timezone.now()
                datoSimulado.append({
                    "valor": ultimoValor + 1 if random.randint(0,1) == 0 else ultimoValor -1,
                    "fechaRegistro": (now - timedelta(seconds=30)).date(),
                    "horaRegistro": (now - timedelta(seconds=30)).time(),
                    "variable": 'humedad'
                })
            sensor_data.append({
                "tipoSensor": sensor.tipoSensor,
                "estado": sensor.estado,
                "ubicacion": sensor.ubicacion,
                "datos": datoSimulado
            })
        
            return Response({"sensores": sensor_data})
        except Plantacion.DoesNotExist:
            return Response({"error": "Plantacion no encontrada"}, status=404)
                                    
class CultivoViewSet(ModelViewSet):
    serializer_class = CultivoSerializer
    queryset = Cultivo.objects.all()

class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class ConfiguracionUmbralViewSet(ModelViewSet):
    queryset = ConfiguracionUmbral.objects.all()
    serializer_class = ConfiguracionUmbralSerializer