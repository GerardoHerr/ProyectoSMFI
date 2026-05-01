<template>
  <div>
    <!-- Bienvenida personalizada -->
    <div
      class="bg-gradient-to-r from-green-600 to-green-800 text-white p-8 mb-8"
    >
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold mb-2">Bienvenido, {{ currentUser?.nombre || 'Usuario' }}!</h2>
        <p class="text-green-100">{{ getGreeting() }}</p>
      </div>
    </div>

    <!-- Contenido principal -->
    <div
      class="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      :style="{ backgroundImage: 'url(https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=2000&q=80)'}"
    >
      <div class="absolute inset-0 bg-black/50"></div>
      <div class="relative text-center p-8">
        <h1 class="text-6xl md:text-8xl font-extrabold text-white tracking-wide drop-shadow">SMFI</h1>
        <p class="mt-4 text-gray-200 text-lg">Sistema de Monitoreo de Fincas Inteligentes</p>

        <div class="mt-8 flex justify-center gap-4 flex-wrap">
          <RouterLink to="/plantacion/lista" class="bg-green-600 text-white px-6 py-3 rounded-lg shadow hover:bg-green-700 transition">
            Ver Plantaciones
          </RouterLink>
          <RouterLink to="/plantacion/monitoreo" class="bg-white border border-green-600 text-green-600 px-6 py-3 rounded-lg shadow hover:bg-green-50 transition">
            Monitoreo Plantaciones
          </RouterLink>
        </div>

        <!-- Tarjetas de información del usuario -->
        

        <div class="mt-8 text-xs text-gray-200">Panel de Control - Sistema SMFI v1.0</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import authService from '@/services/authService';

const currentUser = ref(null);

onMounted(() => {
  currentUser.value = authService.getCurrentUser();
});

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) {
    return '¡Buenos días! Comienza tu jornada de monitoreo.';
  } else if (hour < 18) {
    return '¡Buenas tardes! Revisa el estado de tus plantaciones.';
  } else {
    return '¡Buenas noches! Termina tu jornada en SMFI.';
  }
};
</script>