<template>
  <div class="min-h-screen bg-gray-100 flex justify-center py-10">
    <div class="w-full max-w-3xl">

      <!-- Título -->
      <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center flex items-center justify-center gap-2">
        <!-- Icono -->
        <svg xmlns="http://www.w3.org/2000/svg"
             class="w-8 h-8 text-green-600"
             fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 2a10 10 0 00-7.07 17.07c.39.39.92.61 1.48.61H17.6c.56 0 1.09-.22 1.48-.61A10 10 0 0012 2z" />
        </svg>

        Lista de Plantaciones - Monitoreo
      </h1>

      <!-- Cards -->
      <div class="grid gap-4">
        <RouterLink
          v-for="plantacion in plantaciones"
          :key="plantacion.id"
          :to="`/plantacion/grafico`"
          class="block bg-white p-5 rounded-xl shadow-md cursor-pointer
                 hover:shadow-lg hover:border-green-500
                 border border-transparent transition duration-200"
        >
          <div class="flex items-center gap-3">
            <!-- Icono card -->
            <svg xmlns="http://www.w3.org/2000/svg"
                 class="w-6 h-6 text-green-600"
                 fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8c-1.657 0-3 1.567-3 3.5S10.343 15 12 15s3-1.567 3-3.5S13.657 8 12 8z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M5 12c0 5 7 10 7 10s7-5 7-10a7 7 0 10-14 0z" />
            </svg>

            <h2 class="text-xl font-semibold text-gray-800">
              {{ plantacion.nombre }}
            </h2>
          </div>

          <p class="text-gray-600 text-sm mt-2">
            Usuario Responsable: Manuel Lopez
          </p>
        </RouterLink>
      </div>

      <!-- Estado vacío -->
      <p
        v-if="!plantaciones.length"
        class="text-center text-gray-500 mt-8"
      >
        No hay plantaciones registradas
      </p>

    </div>
  </div>
</template>


<script setup>    
import { getPlantaciones, getPlantacionById } from '@/services/PlantacionesService';
import { ref, onMounted } from 'vue';

const plantaciones = ref([]);

onMounted(async () => {
    try {
        const response = await getPlantaciones();
        plantaciones.value = response.data;
    } catch (error) {
        console.error('Error al cargar plantaciones:', error);
    }
});

const seleccionarPlantacion = async (id) => {
    try {
        const response = await getPlantacionById(id);
        console.log('Plantacion seleccionada:', response.data);
    } catch (error) {
        console.error('Error al seleccionar plantacion:', error);
    }
};

</script>