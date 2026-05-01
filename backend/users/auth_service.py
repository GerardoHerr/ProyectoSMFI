from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from django.contrib.auth.models import User
from .models import Usuario

# Instanciar el hasher de Argon2id
ph = PasswordHasher()

class AuthenticationService:
    """
    Servicio de autenticación y hashing de contraseñas usando Argon2id.
    Maneja el registro, verificación y cambio de contraseñas.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash una contraseña usando Argon2id.
        
        Args:
            password (str): Contraseña en texto plano
            
        Returns:
            str: Hash codificado en formato $argon2id$...
                Incluye: algoritmo, versión, parámetros (memoria, iteraciones, paralelismo), salt y hash
        """
        try:
            return ph.hash(password)
        except Exception as e:
            raise ValueError(f"Error al hashear la contraseña: {str(e)}")

    @staticmethod
    def verify_password(password: str, hash_stored: str) -> bool:
        """
        Verifica si la contraseña coincide con el hash almacenado.
        
        Args:
            password (str): Contraseña en texto plano (ingresada por el usuario)
            hash_stored (str): Hash almacenado en la BD (formato $argon2id$...)
            
        Returns:
            bool: True si la contraseña es correcta, False caso contrario
        """
        try:
            ph.verify(hash_stored, password)
            return True
        except VerifyMismatchError:
            # La contraseña no coincide
            return False
        except InvalidHash as e:
            # El hash almacenado está corrupto o es inválido
            raise ValueError(f"Hash inválido en la base de datos: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error al verificar la contraseña: {str(e)}")

    @staticmethod
    def register_user(nombre: str, correo: str, password: str, rol_id: int = None) -> dict:
        """
        Registra un nuevo usuario hashando su contraseña.
        
        Args:
            nombre (str): Nombre del usuario
            correo (str): Email único del usuario
            password (str): Contraseña en texto plano
            rol_id (int, optional): ID del rol asignado
            
        Returns:
            dict: {'success': bool, 'usuario': Usuario object, 'message': str}
        """
        try:
            # Verificar que el email no exista
            if Usuario.objects.filter(correo=correo).exists():
                return {
                    'success': False,
                    'message': f'El correo {correo} ya está registrado'
                }
            
            # Hashear la contraseña
            password_hash = AuthenticationService.hash_password(password)
            
            # Crear el usuario
            usuario = Usuario(
                nombre=nombre,
                correo=correo,
                password_hash=password_hash,
                rol_id=rol_id,
                isActivo=True
            )
            usuario.save()
            
            return {
                'success': True,
                'usuario': usuario,
                'message': 'Usuario registrado exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al registrar usuario: {str(e)}'
            }

    @staticmethod
    def authenticate_user(correo: str, password: str) -> dict:
        """
        Autentica un usuario verificando su correo y contraseña.
        
        Args:
            correo (str): Email del usuario
            password (str): Contraseña en texto plano
            
        Returns:
            dict: {'success': bool, 'usuario': Usuario object, 'message': str}
        """
        try:
            # Buscar el usuario por correo
            usuario = Usuario.objects.get(correo=correo)
            
            if not usuario.isActivo:
                return {
                    'success': False,
                    'message': 'Usuario inactivo'
                }
            
            # Verificar la contraseña
            if AuthenticationService.verify_password(password, usuario.password_hash):
                return {
                    'success': True,
                    'usuario': usuario,
                    'message': 'Autenticación exitosa'
                }
            else:
                return {
                    'success': False,
                    'message': 'Contraseña incorrecta'
                }
        except Usuario.DoesNotExist:
            return {
                'success': False,
                'message': 'Usuario no encontrado'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error durante la autenticación: {str(e)}'
            }

    @staticmethod
    def change_password(usuario_id: int, old_password: str, new_password: str) -> dict:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            usuario_id (int): ID del usuario
            old_password (str): Contraseña actual en texto plano
            new_password (str): Nueva contraseña en texto plano
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Verificar la contraseña antigua
            if not AuthenticationService.verify_password(old_password, usuario.password_hash):
                return {
                    'success': False,
                    'message': 'Contraseña actual incorrecta'
                }
            
            # Hashear y guardar la nueva contraseña
            new_hash = AuthenticationService.hash_password(new_password)
            usuario.password_hash = new_hash
            usuario.save()
            
            return {
                'success': True,
                'message': 'Contraseña actualizada exitosamente'
            }
        except Usuario.DoesNotExist:
            return {
                'success': False,
                'message': 'Usuario no encontrado'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al cambiar contraseña: {str(e)}'
            }
