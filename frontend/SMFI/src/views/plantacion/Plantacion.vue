<template>
  <!-- CONTENEDOR PRINCIPAL (ANCHOR DE TODO EL CONTENIDO) -->
  <div v-if="plantacion && cultivo" class="max-w-6xl mx-auto p-6 space-y-6">

    <div 
      v-if="alerta"
      class="bg-white border-l-4 p-4 rounded-xl shadow-md"
      :class="alerta.tipo === 'bajo'
        ? 'border-blue-500'
        : 'border-yellow-500'"
    >
      <div class="flex items-start gap-3">
        <!-- Icono -->
        <svg v-if="alerta.tipo === 'bajo'"
             class="w-6 h-6 text-blue-600"
             fill="none" stroke="currentColor" stroke-width="2"
             viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 8v4m0 4h.01M4.93 4.93l14.14 14.14"/>
        </svg>

        <svg v-else
             class="w-6 h-6 text-yellow-600"
             fill="none" stroke="currentColor" stroke-width="2"
             viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 9v2m0 4h.01M5.07 19h13.86"/>
        </svg>

        <div class="flex-1">
          <p class="font-semibold text-gray-800">
            {{ alerta.mensaje }}
          </p>
          <p class="text-sm text-gray-600 mt-1">
            {{ alerta.recomendacion }}
          </p>

          <button
            class="mt-3 px-4 py-2 rounded-lg text-white text-sm font-medium"
            :class="alerta.tipo === 'bajo'
              ? 'bg-blue-600 hover:bg-blue-700'
              : 'bg-yellow-600 hover:bg-yellow-700'"
            @click="ejecutarAccion(alerta.accion)"
          >
            {{ alerta.accion }}
          </button>
        </div>
      </div>
    </div>

    <!-- Card Plantación -->
    <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <div class="flex items-center gap-2 mb-4">
        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor"
             stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 2C8 6 6 10 6 14a6 6 0 0012 0c0-4-2-8-6-12z"/>
        </svg>

        <h2 class="text-2xl font-bold text-gray-800">
          Detalles de la Plantación
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
        <p><span class="font-semibold">Nombre:</span> {{ plantacion.nombre }}</p>
        <p><span class="font-semibold">Fecha:</span> {{ plantacion.fechaRegistro }}</p>
        <p><span class="font-semibold">Espacio:</span> {{ plantacion.espacio }} KM</p>
        <p><span class="font-semibold">Cultivo:</span> {{ cultivo.nombreCultivo }}</p>
        <p>
          <span class="font-semibold">Sensores activos:</span>
          {{ sensores.length }}
        </p>
      </div>
    </div>

    <!-- Sensores -->
    <div>
      <div class="flex items-center gap-2 mb-4">
        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor"
             stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M8.53 16.11a6 6 0 006.94 0M5.07 12.66a10 10 0 0013.86 0M2.1 9.19a14 14 0 0019.8 0"/>
        </svg>

        <h3 class="text-xl font-semibold text-gray-800">
          Sensores
        </h3>
      </div>

      <div v-if="sensores.length"
           class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

        <div
          v-for="sensor in sensores"
          :key="sensor.id"
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition"
        >
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-lg font-bold text-gray-800">
              {{ sensor.tipoSensor }}
            </h4>

            <span class="text-xs px-2 py-1 rounded-full bg-green-100 text-green-700">
              Activo
            </span>
          </div>

          <div class="flex items-center gap-2 text-gray-600 text-sm mb-2">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor"
                 stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 11a3 3 0 100-6 3 3 0 000 6z"/>
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M19.5 11c0 7-7.5 11-7.5 11S4.5 18 4.5 11a7.5 7.5 0 1115 0z"/>
            </svg>

            <span>{{ sensor.ubicacion }}</span>
          </div>

          <div class="mt-4">
            <p class="text-sm text-gray-500">Último valor registrado</p>

            <p v-if="ultimoValor(sensor)"
               class="text-2xl font-bold text-blue-600">
              {{ ultimoValor(sensor).valor }}
            </p>

            <p v-else class="text-sm text-gray-400 italic">
              Sin datos registrados
            </p>
          </div>
        </div>

      </div>

      <div v-else class="text-gray-500 italic">
        No hay sensores registrados en esta plantación.
      </div>
    </div>

  </div>

  <!-- CARGA -->
  <div v-else class="p-6 text-center text-gray-500">
    Cargando plantación...
  </div>
</template>


<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getPlantacionById, getSensoresByPlantacionId } from '@/services/PlantacionesService';
import { getCultivoById } from '@/services/CultivoService';
import {getConfiguracionUmbralById} from '@/services/ConfiguracionUmbralService';
import { crearAlerta, listarAlertas, modificarAlerta } from '@/services/AlertaService';

const route = useRoute();
const id = route.params.id; 

const plantacion = ref(null);
const cultivo = ref(null);
const sensores = ref([]);
const configuracionUmbral = ref(null);
const alerta = ref(null);
const alertaActiva = ref(false);
let valorBase = ref(35); // Valor base inicial
const valorManual = ref(false);

const ultimoValor = (sensor) => {
    if (sensor.datos && sensor.datos.length > 0) {
        return sensor.datos[sensor.datos.length - 1];
    }
    return null;
}

const verificarUmbral = async (valor) => {
  if (!configuracionUmbral.value || !plantacion.value) return;

  const valorMinimo = configuracionUmbral.value.valorMinimo;
  const valorMaximo = configuracionUmbral.value.valorMaximo;

  // 🔒 evitar alertas repetidas
  if (alertaActiva.value) return;

  /* =========================
     📉 VALOR BAJO → RIEGO
     ========================= */
  if (valor < valorMinimo) {
    try {
      const res = await listarAlertas();
      const existente = res.data.find(
        a =>
          a.plantacion === plantacion.value.id &&
          a.tipoAlerta === 'riego' &&
          a.estado === 'pendiente'
      );

      if (existente) {
        alertaActiva.value = true;
        alerta.value = {
          id: existente.id, // ⬅️ id REAL
          tipo: 'bajo',
          mensaje: 'Valor por debajo del umbral mínimo',
          recomendacion: 'Se recomienda realizar riego',
          accion: 'Riego'
        };
        console.warn('Alerta de riego ya existente');
        return;
      }
    } catch (e) {
      console.warn('No se pudieron comprobar alertas existentes', e);
    }

    alertaActiva.value = true;

    try {
      const res = await crearAlerta({
        tipoAlerta: 'riego',
        descripcion: 'Valor por debajo del umbral mínimo',
        plantacion: plantacion.value.id,
        recomendacion: 1,
      });

      alerta.value = {
        id: res.data.id, // ⬅️ id guardado
        tipo: 'bajo',
        mensaje: 'Valor por debajo del umbral mínimo',
        recomendacion: 'Se recomienda realizar riego',
        accion: 'Riego'
      };
    } catch (error) {
      alertaActiva.value = false;
      console.warn('Error creando alerta:', error.response?.data);
    }

  /* =========================
     📈 VALOR ALTO → SECADO
     ========================= */
  } else if (valor > valorMaximo) {
    try {
      const res = await listarAlertas();
      const existente = res.data.find(
        a =>
          a.plantacion === plantacion.value.id &&
          a.tipoAlerta === 'secado' &&
          a.estado === 'pendiente'
      );

      if (existente) {
        alertaActiva.value = true;
        alerta.value = {
          id: existente.id, // ⬅️ id REAL
          tipo: 'alto',
          mensaje: 'Valor por encima del umbral máximo',
          recomendacion: 'Se recomienda proceso de secado',
          accion: 'Secado'
        };
        console.warn('Alerta de secado ya existente');
        return;
      }
    } catch (e) {
      console.warn('No se pudieron comprobar alertas existentes', e);
    }

    alertaActiva.value = true;

    try {
      const res = await crearAlerta({
        tipoAlerta: 'secado',
        descripcion: 'Valor por encima del umbral máximo',
        plantacion: plantacion.value.id,
        recomendacion: 2,
      });

      alerta.value = {
        id: res.data.id, // ⬅️ id guardado
        tipo: 'alto',
        mensaje: 'Valor por encima del umbral máximo',
        recomendacion: 'Se recomienda proceso de secado',
        accion: 'Secado'
      };
    } catch (error) {
      alertaActiva.value = false;
      console.warn('Error creando alerta:', error.response?.data);
    }

  /* =========================
     ✅ VALOR NORMAL
     ========================= */
  } else {
    alertaActiva.value = false;
    alerta.value = null;
  }
};
const ejecutarAccion = (accion) => {
  console.log(`Acción ejecutada: ${accion}`);
  if (accion === 'Riego') {
    alert('Sistema de riego activado');
    // simular efecto del riego incrementando valorBase
    valorBase.value += 30;
    valorManual.value = true;
  } else if (accion === 'Secado') {
    alert('Sistema de secado activado'); //FALTA AÑADIR ESTE EL   EFFECTO
  }

  modificarAlerta(alerta.value.id, { estado: 'atendida' })
    .then(() => {
      console.log('Alerta marcada como resuelta');
      alertaActiva.value = false;
      alerta.value = null;
      // recargar sensores inmediatamente para reflejar cambio simulado
      cargarDatos();
    })
    .catch((error) => {
      console.error('Error al marcar la alerta como resuelta:', error);
    });
  
};

const cargarDatos = async () => {

   if (!valorManual.value && sensores.value.length > 0) {
    const ultimo = ultimoValor(sensores.value[0]);
    if (ultimo) {
      valorBase.value = ultimo.valor;
    }
  }
  
  const sensoresRes = await getSensoresByPlantacionId(id, valorBase.value);
  sensores.value = sensoresRes.data.sensores; 
  const ultimo = ultimoValor(sensores.value[0]);

  if (ultimo) {
    verificarUmbral(ultimo.valor);
  }

}


onMounted(async () => {
    try {
        const response = await getPlantacionById(id);
        plantacion.value = response.data;
        
        const cultivoId = plantacion.value.cultivo;
        if (cultivoId != null) {
            const cultivoResponse = await getCultivoById(cultivoId);
            cultivo.value = cultivoResponse.data;
            console.log('Cultivo cargado:', cultivo.value);
        }
        
        const idConfig = cultivo.value ? cultivo.value.configuracion : null;
        if (idConfig != null) {
            const configResponse = await getConfiguracionUmbralById(idConfig);
            configuracionUmbral.value = configResponse.data;
            console.log('Configuración Umbral cargada:', configuracionUmbral.value);
        }

        cargarDatos();
        setInterval(cargarDatos, 4000); // Actualiza cada 4 segundos

    } catch (error) {
        console.error('Error al cargar la plantación:', error);
    }
});


</script>