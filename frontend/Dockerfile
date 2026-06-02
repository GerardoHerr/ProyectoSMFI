# ============================================================
#  Hito 7 — Hardening Frontend Vue/Vite (SMFI)
#  Basado en el Dockerfile original del proyecto
# ============================================================

# ── STAGE 1: Builder ─────────────────────────────────────────
# Node solo para instalar dependencias y compilar
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar manifiestos primero (mejor uso de caché de capas)
COPY package*.json ./

# npm ci es más seguro que npm install:
# - usa package-lock.json exacto (reproducible)
# - falla si hay diferencias con el lock
RUN npm ci --frozen-lockfile

# Copiar el código fuente
COPY . .

# Compilar para producción (genera /app/dist)
RUN npm run build


# ── STAGE 2: Runtime ─────────────────────────────────────────
# Para desarrollo: mantener node:20-alpine con usuario no root
FROM node:20-alpine AS runtime

# ── Principio de menor privilegio ────────────────────────────
# node:alpine ya incluye el usuario 'node' (uid 1000)
WORKDIR /app

# Copiar dependencias y código
COPY --chown=node:node package*.json ./
RUN npm ci --frozen-lockfile

# El código fuente lo monta el volumen en desarrollo,
# pero copiamos igual para que funcione sin volumen
COPY --chown=node:node . .

# Cambiar al usuario sin privilegios ANTES de exponer
USER node

EXPOSE 5173

# CMD con --host para que Vite escuche en red (necesario en Docker)
# Solo UN CMD (el original tenía dos, el segundo sobreescribía al primero)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]