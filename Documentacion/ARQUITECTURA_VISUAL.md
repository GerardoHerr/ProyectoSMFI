# 🏗️ ARQUITECTURA DE SMFI - Sistema Completo

## Diagrama General

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          🌐 NAVEGADOR (Usuario)                         │
│                                                                          │
│   https://localhost:5173/login  (SIN ADVERTENCIAS - TLS 1.3)           │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                   📱 FRONTEND (Vue.js + Vite)                    │  │
│   │                                                                  │  │
│   │   • Login.vue → Formulario Email + Contraseña                   │  │
│   │   • Registro.vue → Crear Usuario                                │  │
│   │   • Menu → Mostrar Usuario + Logout                             │  │
│   │   • Inicio.vue → Dashboard Personalizado                        │  │
│   │                                                                  │  │
│   │   Router Guard ┐                                                │  │
│   │   ├─ Si NO auth → /login                                        │  │
│   │   ├─ Si auth → Dejar pasar                                      │  │
│   │   └─ localStorage: {"token": user.id, "usuario": {...}}         │  │
│   │                                                                  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                               ▼                                          │
│                    POST /api/login (HTTPS/TLS 1.3)                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/TLS 1.3
                              │ (Encriptado)
                              │
┌─────────────────────────────────────────────────────────────────────────┐
│                    🔒 PROXY VITE (en dev)                               │
│                   /api → https://localhost:8000/api                    │
│            (Simula comunicación backend en producción)                  │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/TLS 1.3
                              │ (Certificados mkcert)
                              │
┌─────────────────────────────────────────────────────────────────────────┐
│                    🖥️ BACKEND (Django + DRF)                            │
│                     https://localhost:8000                              │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │              📨 ENDPOINTS DE AUTENTICACIÓN                     │   │
│   │                                                                │   │
│   │  POST /api/register/                                           │   │
│   │  ├─ Recibe: nombre, correo, password                          │   │
│   │  ├─ Valida: email único, password 6+ chars                    │   │
│   │  ├─ Hashing: password → Argon2id(salt_random + password)     │   │
│   │  └─ Responde: {"success": true, "usuario": {...}}             │   │
│   │                                                                │   │
│   │  POST /api/login/                                              │   │
│   │  ├─ Recibe: correo, password                                   │   │
│   │  ├─ Busca usuario por email                                    │   │
│   │  ├─ Compara: Argon2id.verify(password, stored_hash)           │   │
│   │  ├─ Si coincide → 200 OK con usuario                           │   │
│   │  └─ Si no → 401 Unauthorized                                   │   │
│   │                                                                │   │
│   │  POST /api/change-password/                                    │   │
│   │  ├─ Verifica old_password (Argon2id)                           │   │
│   │  ├─ Actualiza new_password (nuevo Argon2id)                    │   │
│   │  └─ Responde: {"success": true, "message": "..."}              │   │
│   │                                                                │   │
│   │  GET/PUT/DELETE /api/usuarios/ (CRUD)                          │   │
│   │                                                                │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │            🔐 SEGURIDAD Y CONFIGURACIÓN                       │   │
│   │                                                                │   │
│   │  • TLS 1.3: ssl_context.minimum_version = TLSv1_3             │   │
│   │  • Certificados: mkcert (localhost+1.pem + key)              │   │
│   │  • Cookies: HTTPONLY, SECURE, SAMESITE=Lax                   │   │
│   │  • CORS: Permitir localhost:5173                              │   │
│   │  • HSTS: 1 año de revalidación                                │   │
│   │                                                                │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │              🗄️ BASE DE DATOS (SQLite)                        │   │
│   │                                                                │   │
│   │  Tabla: users_usuario                                          │   │
│   │  ├─ id (PK)                                                    │   │
│   │  ├─ nombre (VARCHAR)                                           │   │
│   │  ├─ correo (VARCHAR, UNIQUE)                                   │   │
│   │  ├─ password_hash (VARCHAR) ← Argon2id encoded string         │   │
│   │  ├─ rol_id (FK)                                                │   │
│   │  ├─ fecha_creacion (TIMESTAMP)                                 │   │
│   │  ├─ fecha_actualizacion (TIMESTAMP)                            │   │
│   │  └─ isActivo (BOOLEAN)                                         │   │
│   │                                                                │   │
│   │  Estructura password_hash:                                     │   │
│   │  $argon2id$v=19$m=65536,t=3,p=4$[SALT]$[HASH]                 │   │
│   │                                                                │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Autenticación Detallado

### 1. REGISTRO (POST /api/register/)

```
USUARIO                          FRONTEND                         BACKEND
   │                                │                               │
   ├─ Click "Crear Cuenta"         │                               │
   │                                │                               │
   │  Completa formulario           │                               │
   │  ┌─ Nombre: Juan Pérez        │                               │
   │  ├─ Email: juan@ejemplo.com   │                               │
   │  ├─ Password: Segura123       │                               │
   │  └─ Confirmar: Segura123      │                               │
   │                                │                               │
   ├─ Click "Crear Cuenta"          │                               │
   │                                ├─ Valida: formulario OK        │
   │                                ├─ POST /api/register/ (HTTPS)  │
   │                                │  {"nombre":"Juan","correo":...│
   │                                │   "password":"Segura123"}      │
   │                                │                        ├─ Valida email único
   │                                │                        ├─ Valida password 6+
   │                                │                        ├─ Genera salt random
   │                                │                        ├─ Argon2id hash
   │                                │                        ├─ Crea Usuario en BD
   │                                │ ← 201 Created              │
   │                                │  {"success":true,          │
   │                                │   "usuario":{...}}         │
   │                                ├─ Guarda en localStorage   │
   │                                ├─ Redirige a /            │
   │ ← Ve el dashboard             │                           │
   │   personalizado                │                           │
```

### 2. LOGIN (POST /api/login/)

```
USUARIO                          FRONTEND                         BACKEND
   │                                │                               │
   ├─ Ingresa email                 │                               │
   ├─ Ingresa contraseña            │                               │
   │                                │                               │
   ├─ Click "Iniciar Sesión"        │                               │
   │                                ├─ POST /api/login/ (HTTPS)     │
   │                                │  {"correo":"juan@...",        │
   │                                │   "password":"Segura123"}      │
   │                                │                        ├─ Busca usuario
   │                                │                        ├─ Obtiene hash almacenado
   │                                │                        ├─ Argon2id.verify(pwd, hash)
   │                                │                        ├─ Coincide? SÍ
   │                                │ ← 200 OK               │
   │                                │  {"success":true,      │
   │                                │   "usuario":...}       │
   │                                ├─ Guarda en localStorage
   │                                │  token = usuario.id
   │                                ├─ Redirige a /
   │ ← Dashboard visible           │                       │
   │                                │                       │
   │ ¿Contraseña incorrecta?       │                       │
   │                                ├─ POST /api/login/     │
   │                                │  (contraseña mal)      │
   │                                │                  ├─ Argon2id.verify → FALSE
   │                                │ ← 401 Unauthorized │
   │                                ├─ Muestra error   │
   │ ← "Email o contraseña incorrecta"
```

### 3. ACCESO A PÁGINAS PROTEGIDAS (Router Guard)

```
USUARIO                          FRONTEND                         BACKEND
   │                                │                               │
   ├─ Click en "Monitoreo"         │                               │
   │                                ├─ Router Guard:               │
   │                                │  ¿Hay token en localStorage?  │
   │                                │  SÍ → Dejar pasar             │
   │                                ├─ Muestra página              │
   │                                ├─ Si necesita datos:           │
   │                                │  GET /api/plantaciones/ (auth)│
   │                                │                        ├─ Verifica token
   │                                │ ← Datos        │
   │                                ├─ Renderiza página
   │ ← Ve datos del monitoreo      │               │
   │                                │               │
   │ ¿NO hay token?                │               │
   │                                ├─ Router Guard:
   │                                │  ¿Hay token? NO
   │                                │  → Redirige a /login
   │ ← Ve página de login          │
```

---

## Arquitectura de Seguridad

### Capas de Encriptación

```
┌─────────────────────────────────────────────┐
│  1️⃣  NAVEGADOR                              │
│   • HTTPS/TLS 1.3 (RFC 8446)               │
│   • Certificados mkcert (confiables)       │
│   • Handshake 1-RTT (rápido)               │
└──────────────┬──────────────────────────────┘
               │ Encriptado AES-256-GCM
               │
┌──────────────▼──────────────────────────────┐
│  2️⃣  PROXY VITE                             │
│   • Redirige /api → backend                │
│   • Mantiene encriptación                  │
│   • Permite desarrollo sin CORS issues     │
└──────────────┬──────────────────────────────┘
               │ Encriptado AES-256-GCM
               │
┌──────────────▼──────────────────────────────┐
│  3️⃣  BACKEND (Django)                       │
│   • Valida certificate pinning             │
│   • Headers de seguridad                   │
│   • CSRF protection                        │
│   • CORS whitelist                         │
└─────────────────────────────────────────────┘
```

### Protección de Contraseñas

```
CONTRASEÑA DEL USUARIO
    │
    ▼
┌──────────────────────────────┐
│   1. Validación Frontend      │
│   ├─ Min 6 caracteres        │
│   ├─ No vacío                │
│   └─ Confirmar = Password    │
└──────────────┬───────────────┘
               │
               ▼ (HTTPS/TLS 1.3)
┌──────────────────────────────┐
│   2. Transporte Seguro       │
│   ├─ Encriptado AES-256      │
│   ├─ Sin logs en tránsito    │
│   └─ Handshake validado      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│   3. Validación Backend                  │
│   ├─ Valida formato                      │
│   ├─ Comprueba email único               │
│   └─ No se guarda como texto plano       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│   4. Hashing Argon2id                                │
│   ├─ Salt: Generado aleatoriamente (único por user) │
│   ├─ Derivación: 3 iteraciones, 65536 KB memoria    │
│   ├─ Parallelismo: 4 threads                         │
│   ├─ Resistencia: GPU-resistant, timing-safe        │
│   └─ Resultado: $argon2id$v=19$m=....$[hash]        │
└──────────────┬───────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│   5. Almacenamiento en BD                │
│   ├─ Hash + Salt = 1 campo              │
│   ├─ NUNCA contraseña original           │
│   ├─ Imposible revertir                  │
│   └─ Incluso si BD se expone: SEGURA    │
└──────────────────────────────────────────┘
```

---

## Flujo de Sesión (localStorage)

```
ANTES (Sin autenticar)
┌─────────────────────────────┐
│ localStorage                │
│ ├─ token: undefined         │
│ ├─ usuario: undefined       │
│ └─ userRole: undefined      │
└─────────────────────────────┘

DESPUÉS (Login exitoso)
┌─────────────────────────────────────────────┐
│ localStorage                                │
│ ├─ token: "123" (user.id)                  │
│ ├─ usuario: {                              │
│ │  id: 123,                                │
│ │  nombre: "Juan Pérez",                   │
│ │  correo: "juan@ejemplo.com",             │
│ │  rol: 1                                  │
│ │ }                                        │
│ └─ userRole: "1"                           │
└─────────────────────────────────────────────┘

DESPUÉS (Logout)
┌─────────────────────────────┐
│ localStorage (limpio)       │
│ ├─ token: undefined         │
│ ├─ usuario: undefined       │
│ └─ userRole: undefined      │
└─────────────────────────────┘
```

---

## Puntos de Validación

```
┌─────────────────────────────────────────────────────┐
│  PUNTO 1: Validación Cliente (Frontend)            │
│  ────────────────────────────────────────────────   │
│  • Email: formato válido (regex)                   │
│  • Contraseña: 6+ caracteres, confirmación         │
│  • Campos: requeridos                              │
│  • Tipo: se evitan XSS, injection                  │
└─────────────────────────────────────────────────────┘
                      ▼ (HTTPS)
┌─────────────────────────────────────────────────────┐
│  PUNTO 2: Validación Servidor (Backend)            │
│  ────────────────────────────────────────────────   │
│  • Email: requerido, formato válido, único en BD   │
│  • Contraseña: 6+ caracteres                       │
│  • SQL Injection: ORM Django previene              │
│  • CSRF: Token validado                            │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  PUNTO 3: Hashing de Contraseña                    │
│  ────────────────────────────────────────────────   │
│  • Argon2id: con salt único                        │
│  • Nunca en texto plano                            │
│  • Imposible revertir                              │
│  • Resistente a ataques                            │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  PUNTO 4: Almacenamiento Seguro                    │
│  ────────────────────────────────────────────────   │
│  • SQLite encriptado (en desarrollo)               │
│  • Backups protegidos                              │
│  • Acceso: solo Django ORM                         │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  PUNTO 5: Recuperación de Sesión                   │
│  ────────────────────────────────────────────────   │
│  • localStorage: lectura local                     │
│  • Sin exposición a red                            │
│  • Token = user.id (inmutable)                     │
│  • HTTPONLY cookies en backend                     │
└─────────────────────────────────────────────────────┘
```

---

## Configuración en Producción

```
DESARROLLO (Ahora)              PRODUCCIÓN (Futura)
┌──────────────────────────    ┌──────────────────────────
│ Frontend                       │ Frontend
│ • http://localhost:5173        │ • https://tudominio.com
│ • Vite server                  │ • Nginx / Apache
│ • Hot reload                   │ • Minificado
│ • Debug enabled                │ • Gzip compression
│                                │
├──────────────────────────    ├──────────────────────────
│ Backend                        │ Backend
│ • http://localhost:8000        │ • https://api.tudominio.com
│ • Django runserver_plus        │ • Gunicorn / Waitress
│ • Certificados mkcert          │ • Certificados Let's Encrypt
│ • Debug True                   │ • Debug False
│ • Logs a stdout               │ • Logs a archivo
│                                │
├──────────────────────────    ├──────────────────────────
│ BD                             │ BD
│ • SQLite (desarrollo)          │ • PostgreSQL (producción)
│ • Sin contraseña               │ • Con contraseña
│ • En proyecto                  │ • En servidor separado
│                                │
├──────────────────────────    ├──────────────────────────
│ Encriptación                   │ Encriptación
│ • TLS 1.3 (mkcert)             │ • TLS 1.3 (Let's Encrypt)
│ • Sin warnings                 │ • Certificado válido
│ • Local trusted                │ • Browser trusted
│                                │
└──────────────────────────    └──────────────────────────
```

---

## Tecnologías Utilizadas

```
┌──────────────────────────────────────────────────────┐
│  FRONTEND (5173)                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ Vue.js 3.5.26     - Framework UI               │  │
│  │ Vite 7.3.0        - Bundler + dev server       │  │
│  │ Vue Router 4.6.4  - Enrutamiento              │  │
│  │ Axios 1.13.2      - HTTP client                │  │
│  │ TLS 1.3           - Encriptación (mkcert)     │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  BACKEND (8000)                                       │
│  ┌────────────────────────────────────────────────┐  │
│  │ Django 5.2.9           - Framework web         │  │
│  │ DRF 3.15.0             - API REST             │  │
│  │ argon2-cffi 21.3.0     - Password hashing     │  │
│  │ django-cors-headers    - CORS                  │  │
│  │ django-extensions      - runserver_plus       │  │
│  │ Werkzeug 3.0.1         - WSGI app server      │  │
│  │ pyOpenSSL 24.0.0       - SSL/TLS support      │  │
│  │ TLS 1.3                - Encriptación         │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  CERTIFICADOS                                         │
│  ┌────────────────────────────────────────────────┐  │
│  │ mkcert        - Generador de certificados     │  │
│  │ Algoritmo     - RSA 2048 bits (TLS 1.3)      │  │
│  │ Válidos para  - localhost, 127.0.0.1, ::1   │  │
│  │ Durabilidad   - 365 días                      │  │
│  │ Confianza     - Local system only             │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

**Documento**: Arquitectura SMFI v1.0
**Última actualización**: 29 de Abril de 2026
**Versión**: Completa
**Estado**: Documentado ✅
