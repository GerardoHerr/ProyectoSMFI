# Dockerización - Proyecto SMFI

## 📦 Configuración Docker

Este proyecto ha sido dockerizado para facilitar el desarrollo y despliegue. Incluye:

- **Backend**: Django 5.2.9 con Python 3.11
- **Frontend**: Vite + React con Node.js 20
- **Base de Datos**: MySQL 8.0

## 🚀 Inicio Rápido

### 1. Clonar o preparar el proyecto
```bash
cd c:\Users\LENOVO\Desktop\DockerSGTA\ProyectoSMFI
```

### 2. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# (Opcional) Editar .env con tus valores específicos
```

### 3. Iniciar los contenedores
```bash
docker compose up -d
```

Esto iniciará:
- MySQL en puerto 3306
- Backend (Django) en puerto 8000
- Frontend (Vite) en puerto 5173

### 4. Acceder a la aplicación
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **MySQL**: localhost:3306

## 📝 Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker compose logs -f

# Solo del backend
docker compose logs -f backend

# Solo del frontend
docker compose logs -f frontend

# Solo de la BD
docker compose logs -f db
```

### Ejecutar migraciones
```bash
docker compose exec backend python manage.py migrate
```

### Crear superusuario (admin)
```bash
docker compose exec backend python manage.py createsuperuser
```

### Detener contenedores
```bash
docker compose down
```

### Detener y eliminar volúmenes (cuidado: borra datos de BD)
```bash
docker compose down -v
```

### Reconstruir imágenes
```bash
docker compose up -d --build
```

## 🔧 Configuración de Variables de Entorno

Edita el archivo `.env` para personalizar:

```
# Base de datos
DB_ROOT_PASSWORD=root
DB_NAME=smfi_db
DB_USER=smfi_user
DB_PASSWORD=smfi_password

# Django
DEBUG=True  # Cambiar a False en producción
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=cambiar-en-producción

# Frontend
VITE_API_URL=http://localhost:8000
```

## 📦 Estructura de archivos creados

```
ProyectoSMFI/
├── docker-compose.yml      # Configuración de Docker Compose
├── .env.example            # Ejemplo de variables de entorno
├── .dockerignore           # Archivos a ignorar en build
├── backend/
│   └── Dockerfile          # Imagen para Django
└── frontend/
    └── Dockerfile          # Imagen para Vite + React
```

## 🐛 Solución de Problemas

### Los contenedores no inician
- Verifica que los puertos 3306, 8000, 5173 estén disponibles
- Revisa los logs: `docker-compose logs`

### Errores de conexión a BD
- Verifica que `db` esté saludable: `docker-compose ps`
- Espera a que MySQL esté listo (puede tardar 10-15 segundos)

### Cambios en el código no se reflejan
- Los volúmenes están configurados para desarrollo
- Si cambias dependencias, reconstruye: `docker-compose up -d --build`

### Puerto ya en uso
- Modifica los puertos en `docker-compose.yml`:
  ```yaml
  ports:
    - "8001:8000"  # Cambiar host port
  ```

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Django Deployment](https://docs.djangoproject.com/en/5.2/deployment/)

---

**Nota**: En producción, cambia `DEBUG=False`, actualiza `SECRET_KEY` y configura `ALLOWED_HOSTS` apropiadamente.
