from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import plantacionViewSet, CultivoViewSet, SensorViewSet, PlantacionSensoresView, ConfiguracionUmbralViewSet

router = DefaultRouter()
router.register(r'plantaciones', plantacionViewSet, basename='plantacion')
router.register(r'cultivos', CultivoViewSet, basename='cultivo')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'configuraciones-umbral', ConfiguracionUmbralViewSet, basename='configuracionumbral')

urlpatterns = [
    path('', include(router.urls)),
    path('plantaciones/<int:plantacion_id>/sensores/<int:ultimoValor>', PlantacionSensoresView.as_view(), name='plantacion-sensores'),
] 