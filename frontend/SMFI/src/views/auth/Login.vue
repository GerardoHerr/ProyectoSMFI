<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Card Principal -->
      <div class="bg-white rounded-lg shadow-2xl p-8">
        <!-- Logo/Encabezado -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-800 mb-2">SMFI</h1>
          <p class="text-gray-600">Sistema de Monitoreo de Fincas Inteligente</p>
        </div>

        <!-- Formulario de Login -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email -->
          <div>
            <label for="correo" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico
            </label>
            <input
              id="correo"
              v-model="formData.correo"
              type="email"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
              placeholder="tu@email.com"
            />
          </div>

          <!-- Contraseña -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
              placeholder="••••••••"
            />
          </div>

          <!-- Mensaje de Error -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ errorMessage }}
          </div>

          <!-- Mensaje de Éxito -->
          <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
            {{ successMessage }}
          </div>

          <!-- Botón de Login -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center"
          >
            <span v-if="!isLoading">Iniciar Sesión</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Cargando...
            </span>
          </button>
        </form>

        <!-- Separador -->
        <div class="my-6 flex items-center">
          <div class="flex-1 border-t border-gray-300"></div>
          <div class="px-4 text-gray-600 text-sm">o</div>
          <div class="flex-1 border-t border-gray-300"></div>
        </div>

        <!-- Link a Registro -->
        <p class="text-center text-gray-600 text-sm">
          ¿No tienes cuenta?
          <router-link
            to="/registro"
            class="text-green-600 hover:text-green-700 font-medium transition"
          >
            Regístrate aquí
          </router-link>
        </p>
      </div>

      <!-- Información Adicional -->
      <div class="mt-8 text-center text-gray-600 text-xs">
        <p>© 2026 Sistema de Monitoreo de Fincas. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';

const router = useRouter();

const formData = ref({
  correo: '',
  password: ''
});

const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleLogin = async () => {
  // Limpiar mensajes
  errorMessage.value = '';
  successMessage.value = '';

  // Validar campos
  if (!formData.value.correo || !formData.value.password) {
    errorMessage.value = 'Por favor completa todos los campos';
    return;
  }

  isLoading.value = true;

  try {
    const result = await authService.login(formData.value.correo, formData.value.password);

    if (result.success) {
      successMessage.value = 'Login exitoso, redirigiendo...';
      
      // Redirigir a la página principal después de 1.5 segundos
      setTimeout(() => {
        router.push('/');
      }, 1500);
    } else {
      errorMessage.value = result.message || 'Error al iniciar sesión';
    }
  } catch (error) {
    console.error('Error:', error);
    errorMessage.value = 'Error al conectar con el servidor';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Estilos adicionales si es necesario */
</style>
