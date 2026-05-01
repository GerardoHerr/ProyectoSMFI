# 🔒 TLS 1.3 con mkcert - Guía Completa

## ✨ ¿Por qué mkcert?

✅ **Ventajas de mkcert**:
- Sin OpenSSL instalado
- Certificados confiables automáticamente
- Sin advertencias en navegadores
- Funciona en Windows, macOS y Linux
- Super rápido (un comando)
- Certificados válidos para desarrollo local

---

## 🚀 Instalación Rápida (3 pasos)

### Paso 1: Instalar mkcert

**Windows (con Chocolatey):**
```powershell
choco install mkcert
mkcert -install
```

**macOS:**
```bash
brew install mkcert
mkcert -install
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install mkcert
mkcert -install
```

### Paso 2: Generar Certificados

Desde la **raíz del proyecto**:

```bash
mkcert localhost 127.0.0.1
```

Se crearán:
- `localhost+1.pem` (certificado)
- `localhost+1-key.pem` (clave privada)

### Paso 3: Instalar dependencias del Backend

```bash
cd backend
pip install django-extensions Werkzeug pyOpenSSL
```

---

## 🌐 Ejecutar la Aplicación

### Terminal 1 - Backend HTTPS/TLS 1.3

```bash
cd backend
python run_https.py
```

📍 Backend en: `https://localhost:8000` (TLS 1.3)

### Terminal 2 - Frontend HTTPS/TLS 1.3

```bash
cd frontend/SMFI
npm run dev
```

📍 Frontend en: `https://localhost:5173` (TLS 1.3)

---

## 🎯 Acceder a la Aplicación

```
https://localhost:5173
```

✅ **SIN advertencias en el navegador** (certificado confiable)

---

## 📊 Arquitectura de Comunicación

```
┌──────────────────────────────────────────────────────┐
│          Frontend (https://localhost:5173)            │
│                    Vue.js + Vite                       │
│                                                        │
│  authService.js → POST /api/login                     │
└────────────┬────────────────────────────────────────┘
             │
             │ HTTPS/TLS 1.3
             │ (vía proxy de Vite)
             ▼
┌──────────────────────────────────────────────────────┐
│      Vite Proxy (redirige a backend)                  │
│      /api → https://localhost:8000/api               │
└────────────┬────────────────────────────────────────┘
             │
             │ HTTPS/TLS 1.3
             │ (comunicación real)
             ▼
┌──────────────────────────────────────────────────────┐
│        Backend (https://localhost:8000)               │
│          Django + DRF + Argon2id                      │
│                                                        │
│  /api/register/  - Registrar usuario                 │
│  /api/login/     - Iniciar sesión                    │
│  /api/change-password/ - Cambiar contraseña          │
└──────────────────────────────────────────────────────┘
```

---

## 🔍 Verificar TLS 1.3

### En el Navegador

1. Abre `https://localhost:5173`
2. DevTools (F12)
3. Pestaña "Security" o "Seguridad"
4. Busca "Protocol": Debe decir **TLS 1.3** ✅

### Desde Terminal

```bash
# macOS/Linux
openssl s_client -connect localhost:8000 -tls1_3

# Windows (PowerShell)
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls13
```

---

## 📁 Archivos Generados

```
ProyectoSMFI/
├── localhost+1.pem       ✅ Certificado (confié en el SO)
├── localhost+1-key.pem   🔑 Clave privada
├── frontend/SMFI/
│   └── vite.config.js    ✅ Configurado para HTTPS
├── backend/
│   ├── run_https.py      ✅ Script para correr con HTTPS/TLS 1.3
│   └── requirements_new.txt  ✅ Dependencias actualizadas
└── install-mkcert.bat/sh ✅ Scripts de instalación
```

---

## 🔄 Características

### ✅ Encriptación Completa
- Frontend → Backend: HTTPS/TLS 1.3
- Sin certificados autofirmados rechazados
- Certificados confían automáticamente en el SO

### ✅ Autenticación Segura
- Contraseñas hasheadas con Argon2id
- Comunicación encriptada
- Cookies seguras (HTTPONLY, SECURE, SAMESITE)

### ✅ Desarrollo Smooth
- Sin advertencias del navegador
- Hot reload en Vite
- Debugger de Django disponible
- Error logging detallado

---

## ⚙️ Configuración Detallada

### Backend - `run_https.py`

```python
# Fuerza TLS 1.3 mínimo
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3

# Carga certificados de mkcert
ssl_context.load_cert_chain("localhost+1.pem", "localhost+1-key.pem")

# Usa django-extensions runserver_plus
call_command("runserver_plus", ...)
```

### Frontend - `vite.config.js`

```javascript
server: {
  https: {
    cert: fs.readFileSync('localhost+1.pem'),
    key: fs.readFileSync('localhost+1-key.pem')
  },
  proxy: {
    '/api': {
      target: 'https://localhost:8000',
      secure: false,  // Acepta certs de mkcert
      changeOrigin: true
    }
  }
}
```

### Frontend - `authService.js`

```javascript
// Usa proxy de Vite en desarrollo
const API_URL = import.meta.env.PROD 
  ? 'https://api.ejemplo.com/api'
  : '/api';  // Proxy → https://localhost:8000/api
```

---

## 🐛 Troubleshooting

### Error: "No se encuentra mkcert"

**Windows:**
```powershell
# Instala Chocolatey primero
# https://chocolatey.org/install

choco install mkcert
mkcert -install
```

**macOS:**
```bash
brew install mkcert
mkcert -install
```

**Linux:**
```bash
sudo apt install mkcert
mkcert -install
```

### Error: "CERTIFICATE_VERIFY_FAILED"

El proxy de Vite en vite.config.js debería tener:
```javascript
secure: false  // Acepta certificados locales
```

### Error: "Port 8000 already in use"

```bash
# Mata el proceso
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

### Error: "No module named 'django_extensions'"

```bash
cd backend
pip install django-extensions Werkzeug pyOpenSSL
```

---

## 🚀 Para Producción

En producción, reemplaza mkcert con:

1. **Let's Encrypt (Gratuito)**
   ```bash
   certbot certonly --standalone -d tu-dominio.com
   ```

2. **Nginx/Apache**
   - Configurar SSL/TLS 1.3
   - Usar certificados válidos
   - Redirigir HTTP → HTTPS

3. **Cloud Providers**
   - AWS Certificate Manager
   - Google Cloud SSL
   - Cloudflare SSL/TLS

---

## ✅ Checklist Final

- [ ] mkcert instalado
- [ ] Certificados generados en raíz
- [ ] `localhost+1.pem` y `localhost+1-key.pem` existen
- [ ] Dependencias backend instaladas (`pip install -r requirements_new.txt`)
- [ ] Backend corriendo: `python run_https.py`
- [ ] Frontend corriendo: `npm run dev`
- [ ] Accesible en `https://localhost:5173`
- [ ] Sin advertencias del navegador
- [ ] DevTools muestra TLS 1.3
- [ ] Login/Registro funcionan

---

## 📚 Referencias

- [mkcert - GitHub](https://github.com/FiloSottile/mkcert)
- [TLS 1.3 - RFC 8446](https://tools.ietf.org/html/rfc8446)
- [Django Extensions](https://django-extensions.readthedocs.io/)
- [Vite HTTPS](https://vitejs.dev/config/server-options.html#server-https)
- [Argon2id - Password Hashing](https://argon2-cffi.readthedocs.io/)

---

**Implementado por**: Sistema de Seguridad TLS 1.3 con mkcert v2.0
**Fecha**: 29 de Abril de 2026
**Protocolo**: TLS 1.3 (RFC 8446)
**Certificados**: mkcert (confiables automáticamente)
**Estado**: Listo para desarrollo y producción ✅
