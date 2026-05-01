from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RegisterAPIView, LoginAPIView, ChangePasswordAPIView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]