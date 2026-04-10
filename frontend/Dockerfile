# Frontend Dockerfile - Vite + Vue
FROM node:20-alpine

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el código fuente (será reemplazado por volúmenes en desarrollo)
COPY . .

# Exponer puerto
EXPOSE 5173

# Ejecutar Vite en modo desarrollo
CMD ["npm", "run", "dev"]

# Comando para ejecutar en desarrollo o servir en producción
CMD ["npm", "run", "dev", "--", "--host"]
