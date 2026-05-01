#!/usr/bin/env node

/**
 * Script para generar certificados SSL/TLS 1.3 autofirmados
 * Sin necesidad de OpenSSL instalado
 * 
 * Uso: npm run gen-certs
 */

import fs from 'fs';
import path from 'path';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import selfsigned from 'selfsigned';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../..');
const certsDir = path.join(projectRoot, 'certs');

console.log('\n=== Generando Certificados SSL/TLS 1.3 ===\n');

// Crear directorio si no existe
if (!fs.existsSync(certsDir)) {
  fs.mkdirSync(certsDir, { recursive: true });
  console.log(`✅ Directorio creado: ${certsDir}`);
}

try {
  // Atributos del certificado
  const attrs = [
    { name: 'commonName', value: 'localhost' },
    { name: 'organizationName', value: 'SMFI' },
    { name: 'countryName', value: 'EC' },
    { name: 'stateOrProvinceName', value: 'Pichincha' },
    { name: 'localityName', value: 'Quito' }
  ];

  // Opciones del certificado
  const options = {
    days: 365,
    keySize: 2048,
    algorithm: 'sha256',
    extensions: [
      {
        name: 'basicConstraints',
        cA: true
      },
      {
        name: 'keyUsage',
        keyCertSign: true,
        digitalSignature: true,
        nonRepudiation: true,
        keyEncipherment: true,
        dataEncipherment: true
      },
      {
        name: 'extKeyUsage',
        serverAuth: true,
        clientAuth: true,
        codeSigning: true,
        timeStamping: true
      },
      {
        name: 'subjectAltName',
        altNames: [
          {
            type: 2,
            value: 'localhost'
          },
          {
            type: 2,
            value: '*.localhost'
          },
          {
            type: 7,
            ip: '127.0.0.1'
          },
          {
            type: 7,
            ip: '::1'
          }
        ]
      }
    ]
  };

  console.log('⏳ Generando certificado autofirmado (esto toma unos segundos)...\n');

  // Generar certificado
  const { private: privateKey, cert } = selfsigned.generate(attrs, options);

  // Guardar archivos
  const keyPath = path.join(certsDir, 'server.key');
  const certPath = path.join(certsDir, 'server.crt');

  fs.writeFileSync(keyPath, privateKey);
  fs.writeFileSync(certPath, cert);

  console.log('✅ Certificados generados exitosamente:\n');
  console.log(`   📄 Certificado:   ${certPath}`);
  console.log(`   🔑 Clave privada: ${keyPath}\n`);

  // Mostrar información del certificado
  console.log('📋 Información del certificado:\n');
  console.log(`   Algoritmo:    TLS 1.3 compatible`);
  console.log(`   Válido por:   365 días`);
  console.log(`   Hostname:     localhost`);
  console.log(`   Organización: SMFI\n`);

  console.log('✅ Los certificados están listos para usar en desarrollo\n');
  console.log('🚀 Próximos pasos:\n');
  console.log('   1. Backend:  python runserver_https.py');
  console.log('   2. Frontend: npm run dev\n');
  console.log('📍 Accede a: https://localhost:5173\n');
  console.log('⚠️  El navegador mostrará una advertencia (certificado autofirmado)');
  console.log('   Haz clic en "Avanzado" → "Continuar de todos modos"\n');

} catch (error) {
  console.error('❌ Error al generar certificados:\n');
  console.error(error.message);
  process.exit(1);
}
