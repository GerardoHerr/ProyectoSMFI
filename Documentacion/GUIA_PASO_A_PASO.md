# 🎯 GUÍA PASO A PASO - Desde Cero

## 👨‍💻 Eres nuevo en SMFI y quieres que funcione en 10 minutos?

Esta guía te lleva de la mano por cada paso. No te preocupes, es fácil.

---

## ⚙️ REQUISITOS PREVIOS

Verifica que tengas instalado:

```bash
# Comprueba Python
python --version
# Debe mostrar: Python 3.8 o superior

# Comprueba Node.js
node --version
npm --version
# Debe mostrar versiones recientes
```

Si falta algo, instala desde:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

---

## 🚀 PASO 1: INSTALAR HERRAMIENTAS (5 min)

### A) Instalar Chocolatey (Windows)

**Solo si NO tienes Chocolatey:**

1. Abre PowerShell **como Administrador**
2. Copia y pega esto:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
3. Espera a que termine
4. Cierra y vuelve a abrir PowerShell

### B) Instalar mkcert

**En PowerShell (como Administrador):**

```powershell
choco install mkcert
```

Responde `Y` cuando pregunte.

✅ ¡Listo! mkcert está instalado

---

## 📜 PASO 2: GENERAR CERTIFICADOS (2 min)

En PowerShell (en la carpeta del proyecto):

```powershell
cd C:\Users\LENOVO\Desktop\CambiosSMFI\ProyectoSMFI
mkcert -install
mkcert localhost 127.0.0.1
```

✅ Se crearán dos archivos:
- `localhost+1.pem` ✓
- `localhost+1-key.pem` ✓

**Estos archivos son "certificados de confianza". No los compartas, son solo para tu máquina.**

---

## 🔧 PASO 3: INSTALAR DEPENDENCIAS (3 min)

### Backend

En PowerShell:

```powershell
cd backend
pip install -r requirements_new.txt
```

Espera a que termine (puede tomar 1-2 min).

✅ Backend listo

### Frontend

En una **NUEVA** PowerShell:

```powershell
cd frontend/SMFI
npm install
```

Espera a que termine (puede tomar 2-3 min).

✅ Frontend listo

---

## 🌐 PASO 4: EJECUTAR LA APLICACIÓN

### Terminal 1: Backend HTTPS

```powershell
cd backend
python run_https.py
```

Deberías ver algo como:
```
Iniciando Django con HTTPS/TLS 1.3 en puerto 8000...
✅ Certificados cargados correctamente
...
Starting development server at https://localhost:8000
Quit the server with CTRL-C.
```

**NO CIERRES ESTA TERMINAL**

### Terminal 2: Frontend HTTPS

Abre una **NUEVA** PowerShell:

```powershell
cd frontend/SMFI
npm run dev
```

Deberías ver algo como:
```
VITE v7.3.0  ready in 456 ms

➜  Local:   https://localhost:5173/
➜  press h to show help
```

**NO CIERRES ESTA TERMINAL**

---

## 🎉 PASO 5: PROBAR LA APLICACIÓN

Abre tu navegador favorito y ve a:

```
https://localhost:5173
```

### ✅ Deberías Ver:

1. **Página de Login**
   - Campo de email
   - Campo de contraseña
   - Botón "Iniciar Sesión"
   - Link a "Crear Cuenta"

2. **SIN ADVERTENCIAS** en el navegador ✨
   - El candado está verde 🔒
   - La URL dice "https://"
   - No hay "Este sitio no es seguro"

### 🧪 Prueba 1: Registrarse

1. Haz clic en "Crear Cuenta" (o ve a `/registro`)
2. Completa:
   - **Nombre**: Juan Pérez
   - **Email**: juan@ejemplo.com
   - **Contraseña**: Segura123
   - **Confirmar**: Segura123
3. Haz clic en "Crear Cuenta"
4. ✅ Deberías ser redirigido al dashboard en 1.5 segundos

### 🧪 Prueba 2: Iniciar Sesión

1. Accede a `https://localhost:5173/login`
2. Ingresa:
   - **Email**: juan@ejemplo.com
   - **Contraseña**: Segura123
3. Haz clic en "Iniciar Sesión"
4. ✅ Deberías ver tu nombre y email en la página de inicio

### 🧪 Prueba 3: Ver Info de Usuario

En la página de inicio (`/inicio`):
- Deberías ver una tarjeta con tu nombre
- Debería mostrar tu email
- Debería mostrar tu ID de usuario
- Debería mostrar estado "Activo"

### 🧪 Prueba 4: Menú

En la parte superior:
- **Con sesión iniciada**: Deberías ver "Bienvenido, Juan" y botón "Cerrar Sesión"
- **Después de logout**: Deberías ver "Iniciar Sesión"

---

## 🔒 VERIFICAR ENCRIPTACIÓN TLS 1.3

1. En el navegador, ve a `https://localhost:5173`
2. Abre **DevTools**: Presiona `F12`
3. Ve a pestaña "**Security**" (o "**Seguridad**")
4. Busca: "**Protocol**"
5. ✅ Deberías ver: **TLS 1.3**

---

## ❌ PROBLEMAS COMUNES

### Error: "mkcert: comando no encontrado"

**Solución**:
```powershell
# Instala Chocolatey primero
# Luego: 
choco install mkcert
```

### Error: "CERTIFICATE_VERIFY_FAILED"

**Solución**: Los certificados no se cargaron bien. Intenta:
```powershell
mkcert -install
```

### Error: "Port 8000 already in use"

**Solución**: Otro programa usa el puerto.
```powershell
# Busca qué usa el puerto
netstat -ano | findstr :8000

# Mata el proceso
taskkill /PID <PID> /F
```

### Error: "django.core.management.CommandError: No module named 'django_extensions'"

**Solución**: Instala las dependencias:
```bash
cd backend
pip install django-extensions Werkzeug pyOpenSSL
```

### Error: "npm: comando no encontrado"

**Solución**: Node.js no está instalado
- Descarga de https://nodejs.org/
- Instala
- Reinicia PowerShell

### "Mi navegador muestra advertencia de certificado"

**Problema**: Probablemente ejecutaste desde otra carpeta y se crearon certificados diferentes.

**Solución**:
```powershell
# Asegúrate de estar en la raíz del proyecto
cd C:\Users\LENOVO\Desktop\CambiosSMFI\ProyectoSMFI

# Verifica que existan los certificados
dir localhost+1*

# Si no existen, crea nuevos
mkcert localhost 127.0.0.1
```

---

## 📁 ¿Dónde están los archivos?

```
C:\Users\LENOVO\Desktop\CambiosSMFI\ProyectoSMFI\
├── localhost+1.pem             ← Certificado (aquí)
├── localhost+1-key.pem         ← Clave privada (aquí)
├── backend/
│   ├── run_https.py            ← Ejecuta esto
│   └── requirements_new.txt     ← Ya instalado
└── frontend/SMFI/
    ├── vite.config.js          ← Configurado
    └── src/
```

---

## 🎯 Siguientes Pasos (Opcional)

Ahora que todo funciona, puedes:

1. **Cambiar contraseña**: En el dashboard, busca "Cambiar Contraseña"
2. **Ver base de datos**: En `backend/`, abre `db.sqlite3` con una herramienta SQL
3. **Explorar el código**:
   - Frontend login: `frontend/SMFI/src/views/auth/Login.vue`
   - Backend login: `backend/users/views.py`
   - Hashing: `backend/users/auth_service.py`

---

## 📚 Documentación Más Detallada

Si necesitas más información:

- **Autenticación completa**: Ver `LOGIN_AUTENTICACION_DOCUMENTACION.md`
- **TLS 1.3 avanzado**: Ver `MKCERT_TLS_1.3_GUIA.md`
- **Resumen técnico**: Ver `RESUMEN_FINAL.md`
- **Validar configuración**: Ejecuta `python validate_config.py`

---

## ✅ CHECKLIST FINAL

- [ ] mkcert instalado
- [ ] Certificados generados (localhost+1.pem y localhost+1-key.pem)
- [ ] Backend instalado (pip install -r requirements_new.txt)
- [ ] Frontend instalado (npm install)
- [ ] Backend ejecutándose en Terminal 1 (python run_https.py)
- [ ] Frontend ejecutándose en Terminal 2 (npm run dev)
- [ ] Navegador accede a https://localhost:5173 SIN advertencias
- [ ] Puedo registrarme exitosamente
- [ ] Puedo iniciar sesión
- [ ] DevTools muestra TLS 1.3

---

## 🎉 ¡LISTO!

Tu aplicación SMFI está corriendo de forma **segura con TLS 1.3** y **autenticación con Argon2id**.

**Resumen de lo que conseguiste:**
- ✅ Backend Django con autenticación segura
- ✅ Frontend Vue.js con UI profesional
- ✅ Encriptación HTTPS/TLS 1.3
- ✅ Contraseñas hasheadas con Argon2id
- ✅ Certificados de confianza local

**¿Necesitas ayuda?**
- Revisa los documentos markdown
- Ejecuta `python validate_config.py` para validar
- Lee los comentarios en el código

---

**Documento**: Guía Paso a Paso SMFI v1.0
**Última actualización**: 29 de Abril de 2026
**Tiempo estimado**: 10 minutos
**Nivel**: Principiante (todo automatizado)
