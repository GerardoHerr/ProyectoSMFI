<template>
  <nav class="bg-slate-800 text-white px-6 py-3 flex justify-between items-center">
    <h1 class="text-xl font-bold">SMFI</h1>
    <ul class="flex gap-6">
      <router-link to="/">Inicio</router-link>
      <router-link to="/plantacion/lista">ListaPlantación</router-link>
      <router-link to="/plantacion/monitoreo">MonitoreoPlantacion</router-link>
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';

</script>