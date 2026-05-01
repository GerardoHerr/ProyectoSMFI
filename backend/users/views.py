
from datetime import timedelta
import random
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from .models import Usuario
from .serializables import UsuarioSerializer
from .auth_service import AuthenticationService
from django.utils import timezone

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class RegisterAPIView(APIView):
    """
    Endpoint para registrar un nuevo usuario.
    
    POST /api/register/
    Body: {
        "nombre": "string",
        "correo": "string@example.com",
        "password": "string",
        "rol_id": int (opcional)
    }
    """
    
    def post(self, request):
        try:
            nombre = request.data.get('nombre')
            correo = request.data.get('correo')
            password = request.data.get('password')
            rol_id = request.data.get('rol_id')
            
            # Validaciones básicas
            if not all([nombre, correo, password]):
                return Response(
                    {'success': False, 'message': 'Faltan campos requeridos: nombre, correo, password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar largo de contraseña
            if len(password) < 6:
                return Response(
                    {'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el servicio de autenticación
            result = AuthenticationService.register_user(nombre, correo, password, rol_id)
            
            if result['success']:
                serializer = UsuarioSerializer(result['usuario'])
                return Response(
                    {'success': True, 'message': result['message'], 'usuario': serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'success': False, 'message': result['message']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Error en el servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginAPIView(APIView):
    """
    Endpoint para autenticar un usuario (login).
    
    POST /api/login/
    Body: {
        "correo": "string@example.com",
        "password": "string"
    }
    """
    
    def post(self, request):
        try:
            correo = request.data.get('correo')
            password = request.data.get('password')
            
            # Validaciones básicas
            if not all([correo, password]):
                return Response(
                    {'success': False, 'message': 'Faltan campos requeridos: correo, password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el servicio de autenticación
            result = AuthenticationService.authenticate_user(correo, password)
            
            if result['success']:
                serializer = UsuarioSerializer(result['usuario'])
                return Response(
                    {'success': True, 'message': result['message'], 'usuario': serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'success': False, 'message': result['message']},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Error en el servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordAPIView(APIView):
    """
    Endpoint para cambiar la contraseña de un usuario.
    
    POST /api/change-password/
    Body: {
        "usuario_id": int,
        "old_password": "string",
        "new_password": "string"
    }
    """
    
    def post(self, request):
        try:
            usuario_id = request.data.get('usuario_id')
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            # Validaciones básicas
            if not all([usuario_id, old_password, new_password]):
                return Response(
                    {'success': False, 'message': 'Faltan campos requeridos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar largo de nueva contraseña
            if len(new_password) < 6:
                return Response(
                    {'success': False, 'message': 'La nueva contraseña debe tener al menos 6 caracteres'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el servicio de autenticación
            result = AuthenticationService.change_password(usuario_id, old_password, new_password)
            
            if result['success']:
                return Response(
                    {'success': True, 'message': result['message']},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'success': False, 'message': result['message']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Error en el servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )