#!/bin/bash

# Script para esperar a que MySQL esté disponible
# Uso: ./wait-for-db.sh

set -e

host="$DB_HOST"
port="$DB_PORT"
user="$DB_USER"
password="$DB_PASSWORD"

echo "Esperando a que MySQL esté disponible en $host:$port..."

counter=0
max_attempts=30

until nc -z "$host" "$port" 2>/dev/null; do
  counter=$((counter + 1))
  if [ $counter -ge $max_attempts ]; then
    echo "Error: MySQL no está disponible después de $max_attempts intentos"
    exit 1
  fi
  echo "Intento $counter/$max_attempts: MySQL no está disponible aún... esperando 2 segundos"
  sleep 2
done

echo "MySQL está disponible en $host:$port"

# Esperar un poco más para asegurar que está completamente listo
sleep 3

echo "Iniciando aplicación..."
exec "$@"
