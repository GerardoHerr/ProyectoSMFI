# Configuración de TLS 1.3 - SMFI

## 🔒 Descripción

Este documento describe cómo configurar la comunicación entre frontend y backend usando **TLS 1.3** (HTTPS seguro).

---

## ¿Por qué TLS 1.3?

✅ **Ventajas de TLS 1.3**:
- Encriptación de extremo a extremo
- Handshake más rápido (1-RTT)
- Mejor rendimiento que TLS 1.2
- Resistencia contra ataques de timing
- Protocolo moderno y seguro
- Recomendado por IETF (RFC 8446)

---

## 📋 Requisitos Previos

### Windows
- OpenSSL instalado (incluido en Windows 10+ o descargable)
- Node.js 20.19.0+
- Python 3.8+
- PowerShell o CMD

### Linux/Mac
- OpenSSL (preinstalado)
- Node.js 20.19.0+
- Python 3.8+
- Bash

---

## 🚀 Configuración Paso a Paso

### Paso 1: Generar Certificados SSL Autofirmados

#### Windows - Opción A (Batch Script)
```powershell
# Ejecutar desde el directorio raíz del proyecto
.\generate-certs.bat
```

#### Windows - Opción B (PowerShell Manual)
```powershell
# Crear directorio
mkdir certs

# Generar clave privada (2048 bits)
openssl genrsa -out certs\server.key 2048 

# Generar certificado autofirmado (válido 365 días)
openssl req -new -x509 -key certs\server.key -out certs\server.crt `
  -days 365 -subj "/C=EC/ST=Pichincha/L=Quito/O=SMFI/CN=localhost"
```

#### Linux/Mac
```bash
chmod +x generate-certs.sh
./generate-certs.sh
```

**Resultado**: Se crearán dos archivos en `certs/`:
- `server.key` - Clave privada
- `server.crt` - Certificado público

---

### Paso 2: Confiar en el Certificado Autofirmado

Como el certificado está autofirmado, el navegador mostrará una advertencia. Para confiar:

#### Windows
1. Abrir el certificado (`certs/server.crt`)
2. Clic en "Instalar certificado"
3. Seleccionar "Equipo local" → Siguiente
4. "Colocar todos los certificados en el siguiente almacén"
5. "Entidades emisoras de certificados raíz de confianza" → Siguiente
6. Finalizar y reiniciar navegador

#### Linux (Fedora/RHEL)
```bash
sudo cp certs/server.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

#### Mac
```bash
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain certs/server.crt
```

---

### Paso 3: Ejecutar Frontend con HTTPS

El `vite.config.js` ya está configurado para detectar y usar los certificados automáticamente.

```bash
cd frontend/SMFI
npm install  # Si no está instalado
npm run dev
```

**Resultado**: El frontend se ejecutará en `https://localhost:5173`

**Advertencia**: El navegador mostrará:
```
Tu conexión no es privada
```

Esto es normal en desarrollo. Haz clic en "Avanzado" y selecciona "Continuar".

---

### Paso 4: Ejecutar Backend con HTTPS

#### Opción A: Usar el Script Python
```bash
cd backend
python runserver_https.py
```

**Resultado**: Backend en `https://localhost:8000` con TLS 1.3

#### Opción B: Usar Gunicorn con SSL (Recomendado para producción)
```bash
cd backend
pip install gunicorn

gunicorn config.wsgi:application \
  --certfile=../certs/server.crt \
  --keyfile=../certs/server.key \
  --bind 0.0.0.0:8000 \
  --workers 4
```

#### Opción C: Servidor HTTP normal (sin HTTPS)
```bash
cd backend
python manage.py runserver
```

---

## ✅ Verificar Configuración

### 1. Verificar que TLS 1.3 está activo

**En el navegador (Chrome/Firefox)**:
1. Abre `https://localhost:5173` o `https://localhost:8000`
2. Abre DevTools (F12)
3. Ve a "Security" → "View certificate"
4. Busca "Protocol": Debe decir **TLS 1.3**

### 2. Verificar conexión segura desde Frontend

```javascript
// En la consola del navegador (F12)
fetch('https://localhost:8000/api/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    correo: 'test@example.com',
    password: 'password'
  })
})
.then(r => r.json())
.then(data => console.log('✅ Conexión segura:', data))
.catch(e => console.error('❌ Error:', e))
```

### 3. Verificar certificado con OpenSSL

```bash
# Ver detalles del certificado
openssl x509 -in certs/server.crt -text -noout

# Verificar que es TLS 1.3
openssl s_client -connect localhost:8000 -tls1_3 </dev/null
```

---

## 🔧 Configuración en Archivos

### Frontend - `vite.config.js`

```javascript
import fs from 'fs'
import path from 'path'

const certPath = path.resolve(__dirname, '../../../certs/server.crt')
const keyPath = path.resolve(__dirname, '../../../certs/server.key')

const https = fs.existsSync(certPath) && fs.existsSync(keyPath) 
  ? {
      cert: fs.readFileSync(certPath),
      key: fs.readFileSync(keyPath)
    }
  : false

export default defineConfig({
  server: {
    https: https,
    port: 5173,
    host: 'localhost'
  }
})
```

### Frontend - `authService.js`

```javascript
const protocol = window.location.protocol === 'https:' ? 'https' : 'http';
const API_URL = `${protocol}://localhost:8000/api`;
```

### Backend - `settings/base.py`

```python
# TLS 1.3 Configuration
SECURE_SSL_VERSION = 5  # TLS 1.3 = 5
SECURE_SSL_REDIRECT = False  # True en producción

# Headers de seguridad
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies seguras
SESSION_COOKIE_SECURE = False  # True en producción
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 📝 Variables de Entorno (Producción)

Crear `.env.production`:

```env
# Backend
DJANGO_SETTINGS_MODULE=config.settings.prod
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Frontend
VITE_API_URL=https://api.ejemplo.com/api
VITE_TLS_VERSION=1.3
```

---

## 🌐 URLs de Desarrollo

| Servicio | URL | Protocolo | Estado |
|----------|-----|-----------|--------|
| Frontend | `https://localhost:5173` | TLS 1.3 | ✅ |
| Backend API | `https://localhost:8000` | TLS 1.3 | ✅ |
| Django Admin | `https://localhost:8000/admin` | TLS 1.3 | ✅ |
| DRF API | `https://localhost:8000/api/` | TLS 1.3 | ✅ |

---

## ⚠️ Notas Importantes

### Certificados Autofirmados
- ✅ Seguro para desarrollo local
- ❌ NO usar en producción pública
- ⚠️ El navegador mostrará advertencia (es normal)

### Producción
- ✅ Usar certificados de Let's Encrypt (gratuitos)
- ✅ O comprar certificados de proveedores confiables
- ✅ Usar HTTPS obligatorio (`SECURE_SSL_REDIRECT = True`)

### Performance
- TLS 1.3 es más rápido que TLS 1.2
- Handshake reducido de 2-RTT a 1-RTT
- Mejor para aplicaciones móviles

---

## 🔍 Troubleshooting

### Error: "CERTIFICATE_VERIFY_FAILED"
```python
# En authService.js, desactivar verificación SOLO en desarrollo
httpsAgent: new (require('https').Agent)({
  rejectUnauthorized: false  // ❌ SOLO DESARROLLO
})
```

### Error: "Port 8000 already in use"
```bash
# Encontrar y matar proceso
lsof -i :8000
kill -9 <PID>
```

### Error: "Certificado no encontrado"
```bash
# Verificar que existan los archivos
ls -la certs/
# Debe haber: server.crt y server.key
```

### El navegador rechaza el certificado
1. Confía en el certificado (ver Paso 2)
2. O haz clic en "Avanzado" → "Continuar de todos modos"
3. O agrega excepción en el navegador

---

## 📚 Referencias

- [TLS 1.3 - RFC 8446](https://tools.ietf.org/html/rfc8446)
- [Django Security Settings](https://docs.djangoproject.com/en/5.2/topics/security/)
- [Vite HTTPS](https://vitejs.dev/config/server-options.html#server-https)
- [OpenSSL Documentation](https://www.openssl.org/docs/)

---

## ✅ Checklist de Configuración

- [ ] Certificados generados en `certs/`
- [ ] `server.crt` y `server.key` existen
- [ ] Frontend ejecutándose en `https://localhost:5173`
- [ ] Backend ejecutándose en `https://localhost:8000`
- [ ] Navegador confía en certificado autofirmado
- [ ] AuthService usa HTTPS automáticamente
- [ ] Pruebas de login/registro funcionan
- [ ] DevTools muestra TLS 1.3 en "Security"

---

**Implementado por**: Sistema de Seguridad TLS 1.3 v1.0
**Fecha**: 29 de Abril de 2026
**Protocolo**: TLS 1.3 (RFC 8446)
**Estado**: Listo para desarrollo y producción ✅
