<template>
  <div
    class="min-h-screen flex items-center justify-center bg-cover bg-center relative"
    :style="{ backgroundImage: 'url(https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=2000&q=80)'}"
  >
    <div class="absolute inset-0 bg-black/50"></div>
    <div class="relative text-center p-8">
      <h1 class="text-6xl md:text-8xl font-extrabold text-white tracking-wide drop-shadow">SMFI</h1>
      <p class="mt-4 text-gray-200 text-lg">Sistema de Monitoreo de Fincas Inteligentes</p>

      <div class="mt-8 flex justify-center gap-4">
        <RouterLink to="/plantacion/lista" class="bg-green-600 text-white px-6 py-3 rounded-lg shadow hover:bg-green-700">Ver Plantaciones</RouterLink>
        <RouterLink to="/plantacion/monitoreo" class="bg-white border border-green-600 text-green-600 px-6 py-3 rounded-lg shadow hover:bg-green-50">Monitoreo Plantaciones</RouterLink>
      </div>

      <div class="mt-8 text-xs text-gray-200">Bienvenido al panel de SMFI</div>
    </div>
  </div>
</template>

<script setup>
// Página de inicio simple. No se necesita lógica adicional por ahora.
</script>