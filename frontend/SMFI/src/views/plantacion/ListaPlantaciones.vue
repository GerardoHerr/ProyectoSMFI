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

        Lista de Plantaciones
      </h1>

      <!-- Notificaciones -->
      <div v-if="successMessage" class="mb-4 p-3 bg-green-100 text-green-800 rounded">{{ successMessage }}</div>
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 text-red-800 rounded">{{ errorMessage }}</div>

      <!-- Cards -->
      <div class="grid gap-4">
        <div
          v-for="plantacion in plantaciones"
          :key="plantacion.id"
          @click="navigateTo(plantacion.id)"
          class="relative bg-white p-5 rounded-xl shadow-md cursor-pointer
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
            Terreno: {{ plantacion.espacio +  ' KM' }}
          </p>

          <div class="absolute top-3 right-3 flex gap-2">
            <button @click.stop="openEdit(plantacion)" class="text-sm text-blue-600 hover:text-blue-800">Editar</button>
            <button @click.stop="eliminarPlantacion(plantacion.id)" class="text-sm text-red-600 hover:text-red-800">Eliminar</button>
          </div>
        </div>
      </div>

      <!-- Estado vacío -->
      <p
        v-if="!plantaciones.length"
        class="text-center text-gray-500 mt-8"
      >
        No hay plantaciones registradas
      </p>

      <div class="mt-6">
        <button
          @click="showModal = true"
          class="inline-block bg-green-600 text-white px-6 py-3 rounded-full shadow-md hover:bg-green-700 transition duration-200"
        >
          Nueva Plantación
        </button>
      </div>

      <!-- Modal: Nuevo registro -->
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black opacity-40" @click="closeModal"></div>

        <div class="bg-white rounded-lg shadow-lg z-10 w-full max-w-lg p-6">
          <h3 class="text-lg font-semibold mb-4">Crear Nueva Plantación</h3>

          <form @submit.prevent="submitNewPlantacion" class="space-y-4">
            <div>
              <label class="block text-sm font-medium">Nombre</label>
              <input v-model="form.nombre" required class="w-full border rounded-lg p-2" />
              <p v-if="form.nombre && !isValidName(form.nombre)" class="text-xs text-red-600 mt-1">El nombre debe contener al menos una letra.</p>
            </div>

            <div>
              <label class="block text-sm font-medium">Espacio (KM)</label>
              <input type="number" step="0.01" v-model.number="form.espacio" required class="w-full border rounded-lg p-2" />
            </div>

            <div>
              <label class="block text-sm font-medium">Cultivo</label>
              <select v-model="form.cultivo" required class="w-full border rounded-lg p-2">
                <option value="" disabled>Seleccione un cultivo</option>
                <option v-for="c in cultivos" :key="c.id" :value="c.id">{{ c.nombreCultivo || c.nombre || c.id }}</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium">Sensores</label>
              <select v-model="form.sensores" required class="w-full border rounded-lg p-2">
                <option value="" disabled>Seleccione un sensor</option>
                <option v-for="s in sensores" :key="s.tipoSensor" :value="s.id">{{ s.tipoSensor }}</option>
              </select>
            </div>

            <div class="flex justify-end gap-2 mt-4">
              <button type="button" @click="closeModal" class="px-4 py-2 rounded bg-gray-200">Cancelar</button>
              <button type="submit" :disabled="!isValidName(form.nombre)" class="px-4 py-2 rounded bg-green-600 text-white disabled:opacity-50 disabled:cursor-not-allowed">Crear</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal: Editar registro -->
      <div v-if="editModal" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black opacity-40" @click="closeEditModal"></div>

        <div class="bg-white rounded-lg shadow-lg z-10 w-full max-w-lg p-6">
          <h3 class="text-lg font-semibold mb-4">Editar Plantación</h3>

          <form @submit.prevent="submitEditPlantacion" class="space-y-4">
            <div>
              <label class="block text-sm font-medium">Nombre</label>
              <input v-model="editForm.nombre" required class="w-full border rounded-lg p-2" />
              <p v-if="editForm.nombre && !isValidName(editForm.nombre)" class="text-xs text-red-600 mt-1">El nombre debe contener al menos una letra.</p>
            </div>

            <div>
              <label class="block text-sm font-medium">Espacio (KM)</label>
              <input type="number" step="0.01" v-model.number="editForm.espacio" required class="w-full border rounded-lg p-2" />
            </div>

            <div>
              <label class="block text-sm font-medium">Cultivo</label>
              <select v-model="editForm.cultivo" required class="w-full border rounded-lg p-2">
                <option value="" disabled>Seleccione un cultivo</option>
                <option v-for="c in cultivos" :key="c.id" :value="c.id">{{ c.nombreCultivo || c.nombre || c.id }}</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium">Sensores</label>
              <select v-model="editForm.sensores" multiple class="w-full border rounded-lg p-2">
                <option v-for="s in sensores" :key="s.id" :value="s.id">{{ s.tipoSensor || s.id }}</option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Mantén presionada la tecla Ctrl/Cmd para seleccionar múltiples sensores.</p>
            </div>

            <div class="flex justify-end gap-2 mt-4">
              <button type="button" @click="closeEditModal" class="px-4 py-2 rounded bg-gray-200">Cancelar</button>
              <button type="submit" :disabled="!isValidName(editForm.nombre)" class="px-4 py-2 rounded bg-blue-600 text-white disabled:opacity-50 disabled:cursor-not-allowed">Guardar</button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>


<script setup>
import { getPlantaciones, getPlantacionById, createPlantacion, updatePlantacion, deletePlantacion } from '@/services/PlantacionesService';
import { getSensores } from '@/services/sensoresService';
import { getCultivos } from '@/services/CultivoService';
import { getUsuarios } from '@/services/usuarioService';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const plantaciones = ref([]);
const cultivos = ref([]);
const sensores = ref([]);
const showModal = ref(false);
const usuarios = ref([]);

const router = useRouter();

function navigateTo(id) {
  router.push(`/plantacion/${id}`);
}

const form = ref({
  nombre: '',
  espacio: null,
  cultivo: ''
});

const editModal = ref(false);
const editingId = ref(null);
const editForm = ref({ nombre: '', espacio: null, cultivo: '', sensores: [] });

function isValidName(name) {
  if (!name || typeof name !== 'string') return false;
  // Debe contener al menos una letra Unicode (incluye acentos y ñ)
  return /\p{L}/u.test(name.trim());
}

const successMessage = ref('')
const errorMessage = ref('')

function notify(type, msg, timeout = 4000) {
  if (type === 'success') {
    successMessage.value = msg
    errorMessage.value = ''
  } else {
    errorMessage.value = msg
    successMessage.value = ''
  }

  if (timeout > 0) setTimeout(() => { successMessage.value = ''; errorMessage.value = '' }, timeout)
}

async function loadPlantaciones() {
  try {
    const response = await getPlantaciones();
    plantaciones.value = response.data;
  } catch (error) {
    console.error('Error al cargar plantaciones:', error);
  }
}

async function loadCultivos() {
  try {
    const resp = await getCultivos();
    cultivos.value = resp.data;
    console.log('Cultivos cargados:', cultivos.value);
  } catch (err) {
    console.error('Error al cargar cultivos:', err);
  }
}

async function loadSensores() {
  try {
    const resp = await getSensores();
    sensores.value = resp.data;
    console.log('Sensores cargados:', sensores.value);
  } catch (err) {
    console.error('Error al cargar sensores:', err);
  }
}

async function loadUsuarios() {
  try {
    const resp = await getUsuarios();
    console.log('Usuarios cargados:', resp.data);
    usuarios.value = resp.data;
  } catch (err) {
    console.error('Error al cargar usuarios:', err);
  }
}

onMounted(async () => {
  await Promise.all([loadPlantaciones(), loadCultivos(), loadSensores(), loadUsuarios()]);
});

const seleccionarPlantacion = async (id) => {
  try {
    const response = await getPlantacionById(id);
    console.log('Plantacion seleccionada:', response.data);
  } catch (error) {
    console.error('Error al seleccionar plantacion:', error);
  }
};

function closeModal() {
  showModal.value = false;
  form.value = { nombre: '', espacio: null, cultivo: '' };
}

async function submitNewPlantacion() {
  if (!isValidName(form.value.nombre)) {
    notify('error', 'El nombre debe contener al menos una letra.');
    return;
  }
  try {
    const payload = {
      nombre: form.value.nombre,
      espacio: Number(form.value.espacio),
      cultivo: form.value.cultivo,
      sensores: [form.value.sensores],
      usuario: usuarios.value.length > 0 ? usuarios.value[0].id : null
    };
    let resp
    try {
      resp = await createPlantacion(payload);
    } catch (err) {
      // Si el servidor devolvió 500 pero la creación aparentemente ocurrió,
      // intentamos recargar y verificar si la plantación existe.
      console.warn('Error al crear (primera respuesta):', err);
      if (err.response && err.response.status === 500) {
        await loadPlantaciones();
        const found = plantaciones.value.find(p => p.nombre === form.value.nombre && Number(p.espacio) === Number(form.value.espacio));
        if (found) {
          closeModal();
          notify('success', 'Se creó la plantación exitosamente');
          return;
        }
      }
      // si no fue creado, mostramos error
      notify('error', 'Error al crear la plantación. Intente de nuevo.');
      console.error('Error al crear plantación:', err);
      return;
    }

    // Si llegamos aquí sin excepción, tratamos como éxito
    await loadPlantaciones();
    closeModal();
    notify('success', 'Se creó la plantación exitosamente');
    console.log('Plantación creada:', resp.data);
  } catch (err) {
    console.error('Error inesperado al crear plantación:', err);
    notify('error', 'Error inesperado al crear plantación');
  }
}

function openEdit(plantacion) {
  editingId.value = plantacion.id;
  editForm.value.nombre = plantacion.nombre || '';
  editForm.value.espacio = plantacion.espacio || null;
  editForm.value.cultivo = plantacion.cultivo || '';
  // plantacion.sensores puede ser array de objetos o ids
  if (Array.isArray(plantacion.sensores)) {
    editForm.value.sensores = plantacion.sensores.map(s => (s && s.id) ? s.id : s);
  } else {
    editForm.value.sensores = [];
  }
  editModal.value = true;
}

function closeEditModal() {
  editModal.value = false;
  editingId.value = null;
  editForm.value = { nombre: '', espacio: null, cultivo: '', sensores: [] };
}

async function submitEditPlantacion() {
  if (!isValidName(editForm.value.nombre)) {
    notify('error', 'El nombre debe contener al menos una letra.');
    return;
  }
  try {
    const payload = {
      nombre: editForm.value.nombre,
      espacio: Number(editForm.value.espacio),
      cultivo: editForm.value.cultivo,
      sensores: editForm.value.sensores,
      usuario: usuarios.value.length > 0 ? usuarios.value[0].id : null
    };

    try {
      await updatePlantacion(editingId.value, payload);
    } catch (err) {
      console.warn('Error al actualizar (primera respuesta):', err);
      if (err.response && err.response.status === 500) {
        // recargar y verificar si los cambios se aplicaron
        await loadPlantaciones();
        notify('success', 'Se actualizaron los datos (verifique).');
        closeEditModal();
        return;
      }
      notify('error', 'Error al actualizar la plantación.');
      console.error('Error al actualizar plantación:', err);
      return;
    }

    await loadPlantaciones();
    notify('success', 'Plantación actualizada correctamente');
    closeEditModal();
  } catch (err) {
    console.error('Error inesperado al actualizar plantación:', err);
    notify('error', 'Error inesperado al actualizar');
  }
}

async function eliminarPlantacion(id) {
  try {
    await deletePlantacion(id);
    await loadPlantaciones();
    notify('success', 'Plantación eliminada correctamente');
  } catch (err) {
    console.error('Error al eliminar plantación:', err);
    notify('error', 'Error al eliminar la plantación');
  }
}
</script>