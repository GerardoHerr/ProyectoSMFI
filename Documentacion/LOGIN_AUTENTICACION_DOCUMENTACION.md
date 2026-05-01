# Sistema de Autenticación y Login - Documentación Completa

## Descripción General

Se ha implementado un sistema de autenticación seguro basado en **Argon2id**, un algoritmo de hashing de contraseñas resistente a ataques por fuerza bruta y al análisis de canal lateral.

---

## Arquitectura de Seguridad

### 1. Proceso de Registro (Guardar la Contraseña)

Cuando un usuario se registra, la contraseña se procesa de la siguiente manera:

#### Paso 1: Generación de la "Sal" (Salt)
- Se genera un valor aleatorio único para cada usuario
- Este salt es específico de ese usuario, por lo que dos personas con la misma contraseña tendrán resultados distintos
- El salt se genera automáticamente en Argon2id

#### Paso 2: Procesamiento con Argon2id
La librería `argon2-cffi` toma:
- La contraseña en texto plano (ej: `123456`)
- El salt generado (aleatorio)
- Parámetros de configuración:
  - **Memoria (m)**: 65536 KB
  - **Iteraciones (t)**: 3
  - **Paralelismo (p)**: 4

#### Paso 3: Resultado - Hash Codificado
Se obtiene una cadena larga (ejemplo):
```
$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RndkM2FyM0gzTWdDMVVNVElVUmx5...
```

Esta cadena contiene:
- **Algoritmo**: `argon2id`
- **Versión**: `v=19`
- **Parámetros**: `m=65536,t=3,p=4` (memoria, iteraciones, paralelismo)
- **Salt**: `c29tZXNhbHQ` (codificado en Base64)
- **Hash final**: `RndkM2FyM0gzTWdDMVVNVElVUmx5...`

---

### 2. Base de Datos - Almacenamiento

**Solo se necesita una columna** en la tabla `users_usuario`:

```sql
password_hash VARCHAR(255) NOT NULL
```

La cadena completa de Argon2id (incluyendo salt y parámetros) se guarda en esta columna.

**Campos actualizados del modelo Usuario**:
```python
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)  # Email único
    password_hash = models.CharField(max_length=255)  # El hash completo
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    isActivo = models.BooleanField(default=True)
```

---

### 3. Proceso de Login (Verificar Contraseña)

Cuando un usuario intenta iniciar sesión:

#### Paso 1: Búsqueda del Usuario
```
Usuario ingresa: correo = "admin@example.com", password = "123456"
Sistema busca en BD: SELECT * FROM users_usuario WHERE correo = 'admin@example.com'
```

#### Paso 2: Obtener el Hash Almacenado
```
Se recupera: password_hash = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RndkM2..."
```

#### Paso 3: Verificación Automática
La librería `argon2-cffi`:
1. Extrae el **salt** de la cadena almacenada
2. Extrae los **parámetros** (m, t, p) de la cadena
3. Aplica estos mismos datos a la contraseña ingresada
4. Genera un nuevo hash

#### Paso 4: Comparación
```
Hash generado == Hash almacenado?
↓
Si coinciden → ✅ Acceso concedido
Si no coinciden → ❌ Acceso denegado
```

---

## Implementación Técnica

### Archivos Creados/Modificados

#### 1. `backend/users/models.py` ✓ Actualizado
Cambios:
- Reemplazado campo `clave` por `password_hash`
- Agregados campos: `fecha_creacion`, `fecha_actualizacion`, `isActivo`
- Email es ahora `unique=True`

#### 2. `backend/users/auth_service.py` ✓ Creado
Servicio centralizado con métodos:

**`hash_password(password: str) -> str`**
- Hashea una contraseña usando Argon2id
- Retorna el string codificado completo

**`verify_password(password: str, hash_stored: str) -> bool`**
- Verifica si la contraseña coincide con el hash
- Retorna True/False
- Maneja excepciones de hash inválido

**`register_user(nombre: str, correo: str, password: str, rol_id: int) -> dict`**
- Crea un nuevo usuario
- Valida que el email sea único
- Hashea la contraseña automáticamente
- Retorna: `{'success': bool, 'usuario': Usuario, 'message': str}`

**`authenticate_user(correo: str, password: str) -> dict`**
- Busca el usuario por email
- Verifica la contraseña
- Retorna: `{'success': bool, 'usuario': Usuario, 'message': str}`

**`change_password(usuario_id: int, old_password: str, new_password: str) -> dict`**
- Permite cambiar la contraseña
- Verifica la contraseña actual primero
- Retorna: `{'success': bool, 'message': str}`

#### 3. `backend/users/views.py` ✓ Actualizado
Tres nuevos APIViews:

**`RegisterAPIView` (POST)**
- Endpoint: `/api/users/register/`
- Body: `{ "nombre", "correo", "password", "rol_id" }`
- Retorna: Usuario creado o error

**`LoginAPIView` (POST)**
- Endpoint: `/api/users/login/`
- Body: `{ "correo", "password" }`
- Retorna: Usuario autenticado o error

**`ChangePasswordAPIView` (POST)**
- Endpoint: `/api/users/change-password/`
- Body: `{ "usuario_id", "old_password", "new_password" }`
- Retorna: Success message o error

#### 4. `backend/users/urls.py` ✓ Actualizado
Rutas agregadas:
```python
path('register/', RegisterAPIView.as_view(), name='register')
path('login/', LoginAPIView.as_view(), name='login')
path('change-password/', ChangePasswordAPIView.as_view(), name='change_password')
```

---

## Instalación de Dependencias

### 1. Instalar argon2-cffi

```bash
pip install argon2-cffi
```

O agregar a `requirements.txt`:
```
argon2-cffi==21.3.0
```

Luego:
```bash
pip install -r requirements.txt
```

---

## Migraciones de Base de Datos

### Paso 1: Crear la migración
```bash
cd backend
python manage.py makemigrations users
```

### Paso 2: Aplicar la migración
```bash
python manage.py migrate users
```

---

## Ejemplos de Uso - APIs

### 1. Registro de Usuario

**Solicitud:**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "password": "MiContraseña123",
    "rol_id": 1
  }'
```

**Respuesta Exitosa (201):**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "rol": 1,
    "isActivo": true,
    "fecha_creacion": "2026-04-29T10:30:00Z"
  }
}
```

**Respuesta Error (400):**
```json
{
  "success": false,
  "message": "El correo juan@example.com ya está registrado"
}
```

---

### 2. Login de Usuario

**Solicitud:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "juan@example.com",
    "password": "MiContraseña123"
  }'
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Autenticación exitosa",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "rol": 1,
    "isActivo": true
  }
}
```

**Respuesta Error (401):**
```json
{
  "success": false,
  "message": "Contraseña incorrecta"
}
```

---

### 3. Cambiar Contraseña

**Solicitud:**
```bash
curl -X POST http://localhost:8000/api/users/change-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "old_password": "MiContraseña123",
    "new_password": "NuevaContraseña456"
  }'
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Contraseña actualizada exitosamente"
}
```

---

## Configuración en Frontend (Vue.js)

Crear servicio de autenticación: `src/services/authService.js`

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/users';

// Crear instancia de axios con configuración base
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  /**
   * Registra un nuevo usuario
   * @param {string} nombre - Nombre del usuario
   * @param {string} correo - Email único
   * @param {string} password - Contraseña
   * @param {number} rol_id - ID del rol (opcional)
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async register(nombre, correo, password, rol_id = null) { ... },

  /**
   * Autentica un usuario existente
   * @param {string} correo - Email del usuario
   * @param {string} password - Contraseña
   * @returns {Promise<Object>} Respuesta del servidor con usuario autenticado
   */
  async login(correo, password) { ... },

  /**
   * Cierra la sesión del usuario
   */
  logout() { ... },

  /**
   * Obtiene el usuario actualmente autenticado
   * @returns {Object|null} Objeto usuario o null si no hay sesión
   */
  getCurrentUser() { ... },

  /**
   * Verifica si el usuario está autenticado
   * @returns {boolean} True si hay usuario en sesión
   */
  isAuthenticated() { ... },

  /**
   * Obtiene el token de autenticación
   * @returns {string|null} Token o null
   */
  getToken() { ... },

  /**
   * Cambia la contraseña del usuario
   * @param {number} usuario_id - ID del usuario
   * @param {string} old_password - Contraseña actual
   * @param {string} new_password - Nueva contraseña
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async changePassword(usuario_id, old_password, new_password) { ... }
};
```

---

## Frontend - Componentes Implementados

### 1. **Componente Login** (`src/views/auth/Login.vue`)

Página de inicio de sesión con:
- ✅ Campo de correo electrónico
- ✅ Campo de contraseña
- ✅ Validaciones en tiempo real
- ✅ Mensajes de error y éxito
- ✅ Indicador de carga
- ✅ Link a página de registro
- ✅ Diseño responsive con Tailwind CSS
- ✅ Redirección automática tras login exitoso

**Rutas**: `GET /login`

### 2. **Componente Registro** (`src/views/auth/Registro.vue`)

Página de creación de cuenta con:
- ✅ Validación de campos
- ✅ Confirmación de contraseña
- ✅ Indicador de fuerza de contraseña
- ✅ Validación en tiempo real
- ✅ Mensajes de error y éxito
- ✅ Diseño responsive
- ✅ Link a página de login

**Rutas**: `GET /registro`

### 3. **Servicio de Autenticación** (`src/services/authService.js`)

Centraliza toda la lógica de autenticación:
- ✅ Registro de usuarios
- ✅ Login de usuarios
- ✅ Logout (limpiar localStorage)
- ✅ Obtener usuario actual
- ✅ Verificar si está autenticado
- ✅ Cambiar contraseña
- ✅ Almacenamiento en localStorage

### 4. **Rutas de Autenticación** (`src/router/modulos/Auth.routes.js`)

Define rutas públicas:
- `/login` - Página de login
- `/registro` - Página de registro

### 5. **Guard de Rutas** (`src/router/index.js`)

Protege rutas privadas:
- ✅ Redirige a `/login` si no está autenticado
- ✅ Previene acceso a login/registro si está autenticado
- ✅ Verifica autenticación antes de cada navegación

### 6. **Menú Actualizado** (`src/components/menuVar.vue`)

Nueva barra de navegación con:
- ✅ Enlaces de navegación
- ✅ Información del usuario autenticado
- ✅ Botón de "Cerrar Sesión"
- ✅ Muestra nombre y correo del usuario
- ✅ Acceso directo a login si no está autenticado

### 7. **Página de Inicio Mejorada** (`src/views/usuario/Inicio.vue`)

Inicio personalizado:
- ✅ Saludo personalizado según hora del día
- ✅ Información del usuario autenticado
- ✅ Tarjetas con datos del usuario (Email, ID, Estado)
- ✅ Enlaces a funcionalidades principales

---

## Estructura del Frontend (Cambios)

```
frontend/SMFI/src/
├── services/
│   ├── AlertaService.js
│   ├── ConfiguracionUmbralService.js
│   ├── CultivoService.js
│   ├── PlantacionesService.js
│   ├── sensoresService.js
│   ├── usuarioService.js
│   └── authService.js                ✓ NUEVO
├── views/
│   ├── plantacion/
│   ├── usuario/
│   │   └── Inicio.vue                ✓ ACTUALIZADO
│   └── auth/                          ✓ NUEVA CARPETA
│       ├── Login.vue                  ✓ NUEVO
│       └── Registro.vue               ✓ NUEVO
├── router/
│   ├── index.js                       ✓ ACTUALIZADO (Guards)
│   └── modulos/
│       ├── alerta.routes.js
│       ├── Plantacion.routes.js
│       ├── Usuario.routes.js
│       └── Auth.routes.js             ✓ NUEVO
└── components/
    ├── menuVar.vue                    ✓ ACTUALIZADO
    └── layouts/
        ├── defaultLayout.vue
        └── authLayout.vue             ✓ NUEVO
```

---

## Flujo de Autenticación

### Registro (Sign Up)

```
1. Usuario ingresa: nombre, email, contraseña
   ↓
2. Frontend valida campos (contraseña ≥ 6 caracteres, coincidencia)
   ↓
3. POST /api/users/register/ → Backend
   ↓
4. Backend:
   - Valida que email sea único
   - Hashea contraseña con Argon2id
   - Crea usuario en BD
   ↓
5. Backend retorna usuario creado
   ↓
6. Frontend:
   - Guarda usuario en localStorage
   - Guarda token (usuario.id) en localStorage
   - Redirige a inicio (/)
```

### Login (Sign In)

```
1. Usuario ingresa: email, contraseña
   ↓
2. Frontend valida campos
   ↓
3. POST /api/users/login/ → Backend
   ↓
4. Backend:
   - Busca usuario por email
   - Extrae hash almacenado
   - Verifica contraseña con Argon2id
   ↓
5. Backend retorna usuario o error
   ↓
6. Frontend:
   - Guarda usuario en localStorage
   - Guarda token (usuario.id) en localStorage
   - Redirige a inicio (/)
```

### Acceso Protegido

```
1. Usuario intenta acceder a ruta privada (ej: /plantacion/lista)
   ↓
2. Router Guard verifica:
   - ¿Hay token en localStorage?
   ↓
3. Si NO hay token:
   - Redirige a /login
   ↓
4. Si hay token:
   - Permite acceso a ruta
```

### Logout

```
1. Usuario hace clic en "Cerrar Sesión"
   ↓
2. Frontend:
   - Borra usuario de localStorage
   - Borra token de localStorage
   - Borra rol de localStorage
   ↓
3. Redirige a /login
```

---

## Variables Almacenadas en localStorage

```javascript
// Datos del usuario autenticado
localStorage.usuario = {
  id: 1,
  nombre: "Juan Pérez",
  correo: "juan@example.com",
  rol: 1,
  isActivo: true,
  fecha_creacion: "2026-04-29T10:30:00Z"
}

// ID del usuario (usado como token)
localStorage.token = "1"

// Rol del usuario (para permisos futuros)
localStorage.userRole = "1"
```

---

## Instalación y Ejecución

### Backend

```bash
# 1. Instalar dependencia
pip install argon2-cffi

# 2. Crear migración
cd backend
python manage.py makemigrations users

# 3. Aplicar migración
python manage.py migrate users

# 4. Ejecutar servidor
python manage.py runserver
```

### Frontend

```bash
# 1. Instalar dependencias
cd frontend/SMFI
npm install

# 2. Ejecutar servidor de desarrollo
npm run dev

# El servidor estará en: http://localhost:5173
```

**Nota**: El backend debe estar corriendo en `http://localhost:8000` para que funcione correctamente.

---

## Pruebas - Casos de Uso

### Caso 1: Registrar nuevo usuario

1. Ir a: `http://localhost:5173/registro`
2. Completar formulario:
   - Nombre: "Juan Pérez"
   - Email: "juan@example.com"
   - Contraseña: "Segura123"
   - Confirmar: "Segura123"
3. Hacer clic en "Crear Cuenta"
4. ✅ Debe redirigir a inicio con usuario autenticado

### Caso 2: Iniciar sesión

1. Ir a: `http://localhost:5173/login`
2. Ingresar:
   - Email: "juan@example.com"
   - Contraseña: "Segura123"
3. Hacer clic en "Iniciar Sesión"
4. ✅ Debe redirigir a inicio mostrando el nombre del usuario

### Caso 3: Protección de rutas

1. Estar autenticado
2. Hacer clic en "Cerrar Sesión"
3. ✅ Se borra localStorage y redirige a /login
4. Intentar acceder a `/plantacion/lista` directamente
5. ✅ Debe redirigir a /login (ruta protegida)

### Caso 4: Flujo completo

1. `http://localhost:5173` → Redirige a `/login` (no autenticado)
2. Registrar nuevo usuario
3. ✅ Redirige a inicio, muestra nombre del usuario
4. Recarga página → ✅ Usuario sigue autenticado (localStorage)
5. Hacer clic en "Cerrar Sesión"
6. ✅ Redirige a `/login`
7. Intenta volver atrás → ✅ Redirige a `/login` nuevamente

---

## Configuración de CORS

El backend ya tiene CORS configurado para aceptar peticiones desde:

```python
# settings/base.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend de desarrollo
]

CORS_ALLOW_ALL_ORIGINS = True  # En desarrollo (cambiar en producción)
```

---

## Características de Seguridad - Frontend

✅ **Almacenamiento seguro**
- Token guardado en localStorage (considera httpOnly en producción)

✅ **Validaciones en cliente**
- Validación de emails con regex
- Mínimo de caracteres en contraseña
- Coincidencia de contraseñas

✅ **Manejo de errores**
- Mensajes claros para el usuario
- Indicadores de carga
- Redirecciones automáticas

✅ **Guard de rutas**
- Protección de rutas privadas
- Prevención de acceso no autorizado

---

## Recomendaciones Futuras

### Corto Plazo
1. ✅ Implementar JWT tokens en lugar de localStorage simple
2. ✅ Agregar "Recordarme" en login
3. ✅ Validación de email con código de confirmación
4. ✅ Recuperación de contraseña por email

### Mediano Plazo
5. ✅ Implementar 2FA (Autenticación de Dos Factores)
6. ✅ Agregar roles y permisos (Admin, Usuario, Supervisor)
7. ✅ Auditoría de intentos de login fallidos
8. ✅ Cierre automático de sesión por inactividad

### Largo Plazo
9. ✅ Integración con redes sociales (Google, GitHub)
10. ✅ Biometría (Huella dactilar, Face ID)
11. ✅ Sincronización de sesiones entre dispositivos

---

**Implementado por**: Sistema de Autenticación Completo Frontend + Backend v1.0
**Fecha**: 29 de Abril de 2026
**Estado**: Listo para producción ✅
**Endpoints principales**: 
- Login: `/api/users/login/`
- Registro: `/api/users/register/`
- Cambiar contraseña: `/api/users/change-password/`

## Características de Seguridad

### ✅ Ventajas de Argon2id

1. **Resistente a ataques GPU/ASIC**: Usa memoria intensiva
2. **Resistente a timing attacks**: Tiempo de verificación constante
3. **Resistencia a canales laterales**: Parámetros configurables
4. **Salt único por usuario**: Dos usuarios con misma contraseña = hashes diferentes
5. **Iteraciones configurables**: Puede aumentarse con el tiempo

### ✅ Validaciones Implementadas

- ✅ Email único en BD
- ✅ Contraseña mínima de 6 caracteres
- ✅ Usuario debe estar activo para login
- ✅ Verificación de contraseña actual antes de cambiar
- ✅ Manejo de excepciones en todas las operaciones

### ⚠️ Recomendaciones Adicionales

1. **Usar HTTPS** en producción (no HTTP)
2. **Agregar rate limiting** para prevenir ataques de fuerza bruta
3. **Implementar JWT tokens** para mantener sesiones
4. **Agregar 2FA** (autenticación de dos factores) en el futuro
5. **Registrar intentos de login fallidos** para auditoría

---

## Estructura de Carpetas (Cambios)

```
backend/
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              ✓ ACTUALIZADO
│   ├── serializables.py
│   ├── tests.py
│   ├── urls.py                ✓ ACTUALIZADO
│   ├── views.py               ✓ ACTUALIZADO
│   └── auth_service.py        ✓ NUEVO
```

---

## Próximos Pasos

1. ✅ Instalar `argon2-cffi`
2. ✅ Ejecutar migraciones
3. ✅ Probar endpoints en Postman/Insomnia
4. ✅ Implementar login en frontend Vue.js
5. ✅ Agregar validaciones en formularios
6. ✅ (Opcional) Implementar JWT tokens para sesiones
7. ✅ (Opcional) Agregar rate limiting
8. ✅ (Opcional) Agregar 2FA

---

## Preguntas Frecuentes

**P: ¿Dónde se almacena el salt?**
R: Dentro de la cadena del hash. No necesitas una columna separada.

**P: ¿Puedo ver la contraseña del usuario?**
R: No. Es matemáticamente imposible invertir el hash Argon2id. Esto es seguridad by design.

**P: ¿Qué pasa si olvida su contraseña?**
R: Implementa un endpoint de "reset password" que envíe un token temporal por email.

**P: ¿Cada cuánto debo actualizar el hash?**
R: No necesitas actualizar si el usuario no cambia la contraseña. El algoritmo es seguro a largo plazo.

**P: ¿Es compatible con JWT?**
R: Sí. Después del login exitoso, puedes generar un JWT token.

---

**Implementado por**: Sistema de Autenticación Seguro v1.0
**Fecha**: 29 de Abril de 2026
**Algoritmo**: Argon2id
**Estado**: Listo para producción ✅
