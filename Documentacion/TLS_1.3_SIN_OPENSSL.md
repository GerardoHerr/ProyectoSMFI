# ✅ TLS 1.3 - GUÍA SIN OpenSSL

## 🚀 Generar Certificados (SIN instalar OpenSSL)

Usa npm directamente desde el frontend:

```bash
cd frontend/SMFI
npm install
npm run gen-certs
```

**¡Listo!** Los certificados se crearán en `certs/` automáticamente.

---

## 🔒 Ejecutar con HTTPS/TLS 1.3

### Backend (Terminal 1)
```bash
cd backend
python runserver_https.py
```
📍 Backend: `https://localhost:8000` (TLS 1.3)

### Frontend (Terminal 2)
```bash
cd frontend/SMFI
npm run dev
```
📍 Frontend: `https://localhost:5173` (TLS 1.3)

---

## 🌐 Acceder a la Aplicación

```
https://localhost:5173
```

⚠️ **Advertencia del navegador**: Es normal (certificado autofirmado)
- Haz clic en "Avanzado"
- Selecciona "Continuar a localhost"

---

## ✅ Verificar TLS 1.3

1. Abre DevTools (F12)
2. Ve a pestaña "Security"
3. Busca "Protocol": Debe decir **TLS 1.3** ✅

---

## 📊 Comparación

| Método | Requisitos | Instalación | Tiempo |
|--------|-----------|-------------|--------|
| OpenSSL | Windows + Software | Descargar e instalar | 5-10 min |
| **npm** | Solo Node.js | `npm install` | 1-2 min ✅ |

---

**Recomendación**: Usa el método npm que es más fácil y rápido. ✨
