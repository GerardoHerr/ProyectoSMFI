import { fileURLToPath, URL } from 'node:url'
import fs from 'fs'
import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// Ruta a los certificados generados con mkcert (en raíz de ProyectoSMFI)
const projectRoot = path.resolve(__dirname, '../..')
const certPath = path.join(projectRoot, 'localhost+1.pem')
const keyPath = path.join(projectRoot, 'localhost+1-key.pem')

// Verificar si los certificados existen
const https = fs.existsSync(certPath) && fs.existsSync(keyPath) 
  ? {
      cert: fs.readFileSync(certPath),
      key: fs.readFileSync(keyPath)
    }
  : false

// Log para debug
if (!https) {
  console.log('⚠️  HTTPS no disponible. Buscando certificados en:', projectRoot)
  console.log('   Cert:', certPath, 'existe:', fs.existsSync(certPath))
  console.log('   Key:', keyPath, 'existe:', fs.existsSync(keyPath))
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    https: https,
    port: 5173,
    host: 'localhost',
    // Proxy a backend HTTPS
    proxy: {
      '/api': {
        target: 'https://localhost:8000',
        secure: false, // Acepta certificados autofirmados
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
})


