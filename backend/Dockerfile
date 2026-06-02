# ============================================================
#  Hito 7 — Hardening Backend Django (SMFI)
#  Basado en el Dockerfile original del proyecto
# ============================================================

# ── STAGE 1: Builder ─────────────────────────────────────────
# Imagen completa solo para compilar dependencias
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema SOLO para compilar
# (no llegan a la imagen final)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependencias Python en directorio aislado
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── STAGE 2: Runtime ─────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Variables de entorno de seguridad
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar SOLO librerías de runtime necesarias para mysqlclient
# (no build-essential ni pkg-config)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ── Principio de menor privilegio: usuario no root ───────────
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home \
            --shell /usr/sbin/nologin appuser

# Copiar dependencias Python desde el builder
COPY --from=builder /install /usr/local

# Copiar el código
COPY --chown=appuser:appgroup . .

RUN chmod -R 755 /app

# Cambiar al usuario sin privilegios
USER appuser

EXPOSE 8000

# Healthcheck interno
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/admin/login/')" || exit 1

# En producción usar gunicorn; en desarrollo el compose sobreescribe con runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]