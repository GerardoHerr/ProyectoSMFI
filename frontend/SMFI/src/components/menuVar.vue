<template>
  <nav class="bg-slate-800 text-white px-6 py-3 flex justify-between items-center">
    <div class="flex items-center gap-8">
      <h1 class="text-xl font-bold">SMFI</h1>
      <ul class="flex gap-6">
        <router-link to="/" class="hover:text-green-400 transition">Inicio</router-link>
        <router-link to="/plantacion/lista" class="hover:text-green-400 transition">ListaPlantación</router-link>
        <router-link to="/plantacion/monitoreo" class="hover:text-green-400 transition">MonitoreoPlantacion</router-link>
      </ul>
    </div>
    
    <!-- Usuario y Logout -->
    <div class="flex items-center gap-4">
      <div v-if="currentUser" class="flex items-center gap-4">
        <div class="text-sm">
          <p class="font-medium">{{ currentUser.nombre }}</p>
          <p class="text-gray-300 text-xs">{{ currentUser.correo }}</p>
        </div>
        <button
          @click="handleLogout"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition"
        >
          Cerrar Sesión
        </button>
      </div>
      <div v-else>
        <router-link
          to="/login"
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition"
        >
          Iniciar Sesión
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import authService from '@/services/authService';

const router = useRouter();
const currentUser = ref(null);

const updateUser = () => {
  currentUser.value = authService.getCurrentUser();
};

onMounted(() => {
  updateUser();
});

// Actualizar usuario cuando cambia la ruta
watch(() => router.currentRoute.value.path, () => {
  updateUser();
});

const handleLogout = () => {
  authService.logout();
  currentUser.value = null;
  router.push('/login');
};
</script>