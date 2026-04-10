# Frontend Dockerfile - Vite + React
FROM node:20-alpine as builder

WORKDIR /app

# Copiar package.json y package-lock.json
COPY SMFI/package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el código
COPY SMFI/ .

# Build de la aplicación
RUN npm run build

# Etapa de producción
FROM node:20-alpine

WORKDIR /app

# Instalar servidor estático (opcional, para servir archivos)
RUN npm install -g serve

# Copiar los archivos compilados desde la etapa anterior
COPY --from=builder /app/dist ./dist

# Exponer puerto
EXPOSE 5173

# Comando para ejecutar en desarrollo o servir en producción
CMD ["npm", "run", "dev", "--", "--host"]
