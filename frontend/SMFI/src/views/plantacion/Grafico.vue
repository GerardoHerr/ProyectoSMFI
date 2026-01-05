<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-8 text-center">
        Gráfico de Plantaciones
      </h1>
      
      <!-- Panel de Filtros -->
      <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Filtros</h2>
        
        <!-- Variables Ambientales -->
        <div class="mb-6">
          <h3 class="text-sm font-medium text-gray-600 mb-3">Variables Ambientales</h3>
          <div class="flex flex-wrap gap-4">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="filtros.temperatura"
                class="w-5 h-5 text-red-500 rounded focus:ring-2 focus:ring-red-500"
              />
              <span class="text-gray-700 font-medium">Temperatura (°C)</span>
            </label>
            
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="filtros.humedad"
                class="w-5 h-5 text-blue-500 rounded focus:ring-2 focus:ring-blue-500"
              />
              <span class="text-gray-700 font-medium">Humedad (%)</span>
            </label>
          </div>
        </div>
        
        <!-- Rango de Fechas -->
        <div>
          <h3 class="text-sm font-medium text-gray-600 mb-3">Rango de Fechas</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-600 mb-1">Fecha Inicio</label>
              <input
                type="date"
                v-model="filtros.fechaInicio"
                :max="filtros.fechaFin"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm text-gray-600 mb-1">Fecha Fin</label>
              <input
                type="date"
                v-model="filtros.fechaFin"
                :min="filtros.fechaInicio"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Gráfico -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">
          Datos Registrados ({{ datosFiltrados.length }} registros)
        </h2>
        
        <div v-if="!filtros.temperatura && !filtros.humedad" class="h-96 flex items-center justify-center text-gray-500">
          Selecciona al menos una variable para mostrar
        </div>
        
        <div v-else class="w-full h-96">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
      
      <!-- Estadísticas -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        <div v-if="filtros.temperatura" class="bg-white rounded-lg shadow-lg p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Temperatura</h3>
          <div class="space-y-2">
            <p class="text-gray-600">
              Promedio: <span class="font-bold text-red-600">
                {{ estadisticas.temperatura.promedio }}°C
              </span>
            </p>
            <p class="text-gray-600">
              Máxima: <span class="font-bold text-red-600">
                {{ estadisticas.temperatura.maxima }}°C
              </span>
            </p>
            <p class="text-gray-600">
              Mínima: <span class="font-bold text-red-600">
                {{ estadisticas.temperatura.minima }}°C
              </span>
            </p>
          </div>
        </div>
        
        <div v-if="filtros.humedad" class="bg-white rounded-lg shadow-lg p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Humedad</h3>
          <div class="space-y-2">
            <p class="text-gray-600">
              Promedio: <span class="font-bold text-blue-600">
                {{ estadisticas.humedad.promedio }}%
              </span>
            </p>
            <p class="text-gray-600">
              Máxima: <span class="font-bold text-blue-600">
                {{ estadisticas.humedad.maxima }}%
              </span>
            </p>
            <p class="text-gray-600">
              Mínima: <span class="font-bold text-blue-600">
                {{ estadisticas.humedad.minima }}%
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';

// Generar datos simulados para 1 año completo (2024)
const generateData = () => {
  const data = [];
  const startDate = new Date('2024-01-01T00:00:00');
  const endDate = new Date('2024-12-31T23:59:59');
  
  const horasIntervalo = 6;
  const totalRegistros = Math.floor((endDate - startDate) / (horasIntervalo * 60 * 60 * 1000));
  
  for (let i = 0; i < totalRegistros; i++) {
    const date = new Date(startDate);
    date.setHours(startDate.getHours() + i * horasIntervalo);
    
    const mes = date.getMonth();
    const tempBase = 25 + Math.sin((mes - 3) * Math.PI / 6) * 8;
    const humedadBase = 60 - Math.sin((mes - 3) * Math.PI / 6) * 15;
    
    data.push({
      fecha: date.toISOString(),
      temperatura: Math.round((tempBase + (Math.random() - 0.5) * 6) * 10) / 10,
      humedad: Math.round((humedadBase + (Math.random() - 0.5) * 20) * 10) / 10,
    });
  }
  
  return data;
};

// Datos
const allData = ref(generateData());
const chartCanvas = ref(null);
let chartInstance = null;

// Filtros
const filtros = ref({
  temperatura: true,
  humedad: true,
  fechaInicio: '2024-01-01',
  fechaFin: '2024-12-31',
});

// Datos filtrados
const datosFiltrados = computed(() => {
  return allData.value.filter(item => {
    const fecha = new Date(item.fecha);
    const inicio = new Date(filtros.value.fechaInicio);
    const fin = new Date(filtros.value.fechaFin);
    fin.setHours(23, 59, 59);
    
    return fecha >= inicio && fecha <= fin;
  });
});

// Formatear fecha
const formatearFecha = (fecha) => {
  const date = new Date(fecha);
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
};

// Estadísticas
const estadisticas = computed(() => {
  const datos = datosFiltrados.value;
  
  const calcularStats = (valores) => {
    if (valores.length === 0) return { promedio: 0, maxima: 0, minima: 0 };
    return {
      promedio: (valores.reduce((a, b) => a + b, 0) / valores.length).toFixed(1),
      maxima: Math.max(...valores).toFixed(1),
      minima: Math.min(...valores).toFixed(1),
    };
  };
  
  return {
    temperatura: calcularStats(datos.map(d => d.temperatura)),
    humedad: calcularStats(datos.map(d => d.humedad)),
  };
});

// Crear o actualizar el gráfico
const updateChart = () => {
  if (!chartCanvas.value) return;
  
  if (chartInstance) {
    chartInstance.destroy();
  }
  
  const ctx = chartCanvas.value.getContext('2d');
  const datos = datosFiltrados.value;
  
  const datasets = [];
  
  if (filtros.value.temperatura) {
    datasets.push({
      label: 'Temperatura (°C)',
      data: datos.map(d => d.temperatura),
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4,
      pointRadius: 2,
      pointHoverRadius: 5,
    });
  }
  
  if (filtros.value.humedad) {
    datasets.push({
      label: 'Humedad (%)',
      data: datos.map(d => d.humedad),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4,
      pointRadius: 2,
      pointHoverRadius: 5,
    });
  }
  
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: datos.map(d => formatearFecha(d.fecha)),
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index',
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#374151',
          bodyColor: '#374151',
          borderColor: '#e5e7eb',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
        },
      },
      scales: {
        x: {
          grid: {
            display: true,
            color: '#f3f4f6',
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            maxTicksLimit: 12,
          },
        },
        y: {
          grid: {
            display: true,
            color: '#f3f4f6',
          },
          beginAtZero: false,
        },
      },
    },
  });
};

// Watchers
watch([datosFiltrados, () => filtros.value.temperatura, () => filtros.value.humedad], () => {
  nextTick(() => {
    updateChart();
  });
});

// Montar componente
onMounted(() => {
  nextTick(() => {
    updateChart();
  });
});
</script>