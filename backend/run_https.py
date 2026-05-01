#!/usr/bin/env python
"""
Script para ejecutar Django con HTTPS/TLS 1.3

Uso:
    python run_https.py

Certificados:
    - Generados con mkcert (localhost+1.pem y localhost+1-key.pem)
    - Ubicados en la raíz de ProyectoSMFI/
"""

import os
import sys
import django
import ssl
import socket
from pathlib import Path
from wsgiref.simple_server import make_server, WSGIRequestHandler

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.core.wsgi import get_wsgi_application

# Rutas a certificados - En la raíz de ProyectoSMFI
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
CERT_FILE = PROJECT_ROOT / "localhost+1.pem"
KEY_FILE = PROJECT_ROOT / "localhost+1-key.pem"

# Verificar que los certificados existen
if not CERT_FILE.exists() or not KEY_FILE.exists():
    print("❌ ERROR: Certificados no encontrados")
    print(f"   Buscando en: {PROJECT_ROOT}")
    print("")
    print("Genera los certificados ejecutando desde ProyectoSMFI/:")
    print("  Windows: .\\generate-certs.bat")
    print("  macOS/Linux: ./generate-certs.sh")
    sys.exit(1)

print("")
print("🔒 === Iniciando Django con HTTPS/TLS 1.3 ===")
print("")
print(f"📄 Certificado:    {CERT_FILE}")
print(f"🔑 Clave privada:  {KEY_FILE}")
print("")

try:
    # Crear contexto SSL con TLS 1.3
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
    ssl_context.load_cert_chain(str(CERT_FILE), str(KEY_FILE))
    
    print("✅ Contexto SSL/TLS 1.3 configurado correctamente")
    print("")
    print("🚀 Servidor disponible en:")
    print("   https://localhost:8000")
    print("")
    
    # Obtener aplicación WSGI de Django
    application = get_wsgi_application()
    
    # Crear servidor HTTPS
    class QuietWSGIRequestHandler(WSGIRequestHandler):
        def log_message(self, format, *args):
            if "GET" in format or "POST" in format:
                print(f"   {format % args}")
    
    httpd = make_server('localhost', 8000, application, handler_class=QuietWSGIRequestHandler)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    
    print("✅ Servidor HTTPS iniciado")
    print("")
    print("Presiona Ctrl+C para detener")
    print("-" * 50)
    print("")
    
    httpd.serve_forever()
    
except ssl.SSLError as e:
    print(f"❌ Error SSL: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
