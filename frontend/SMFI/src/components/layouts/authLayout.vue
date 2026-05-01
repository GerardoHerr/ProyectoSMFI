<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navegación mínima -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h2 class="text-xl font-bold text-green-600">SMFI</h2>
          </div>
          <div class="flex items-center space-x-4 text-sm text-gray-600">
            <a href="#" class="hover:text-gray-900">Ayuda</a>
            <a href="#" class="hover:text-gray-900">Contacto</a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido Principal -->
    <main>
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center text-gray-600 text-sm">
          <p>© 2026 Sistema de Monitoreo de Fincas Inteligente (SMFI)</p>
          <p class="mt-2">
            <a href="#" class="hover:text-green-600">Privacidad</a> • 
            <a href="#" class="hover:text-green-600">Términos</a> • 
            <a href="#" class="hover:text-green-600">Contacto</a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>
