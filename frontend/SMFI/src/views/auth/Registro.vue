<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Card Principal -->
      <div class="bg-white rounded-lg shadow-2xl p-8">
        <!-- Logo/Encabezado -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-800 mb-2">SMFI</h1>
          <p class="text-gray-600">Crear Nueva Cuenta</p>
        </div>

        <!-- Formulario de Registro -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Nombre -->
          <div>
            <label for="nombre" class="block text-sm font-medium text-gray-700 mb-2">
              Nombre Completo
            </label>
            <input
              id="nombre"
              v-model="formData.nombre"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="Juan Pérez"
            />
          </div>

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
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
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
              minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="Mínimo 6 caracteres"
            />
            <p class="text-xs text-gray-500 mt-1">Mínimo 6 caracteres recomendados</p>
          </div>

          <!-- Confirmar Contraseña -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Contraseña
            </label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              required
              minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="Repite tu contraseña"
            />
          </div>

          <!-- Indicador de Validación de Contraseña -->
          <div v-if="formData.password || formData.confirmPassword" class="p-3 rounded-lg bg-blue-50 border border-blue-200">
            <p v-if="formData.password.length < 6" class="text-xs text-orange-600 flex items-center">
              <span class="mr-2">⚠️</span> Contraseña muy corta (mínimo 6 caracteres)
            </p>
            <p v-else-if="formData.password !== formData.confirmPassword" class="text-xs text-red-600 flex items-center">
              <span class="mr-2">❌</span> Las contraseñas no coinciden
            </p>
            <p v-else class="text-xs text-green-600 flex items-center">
              <span class="mr-2">✅</span> Contraseñas válidas y coinciden
            </p>
          </div>

          <!-- Mensaje de Error -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ errorMessage }}
          </div>

          <!-- Mensaje de Éxito -->
          <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
            {{ successMessage }}
          </div>

          <!-- Botón de Registro -->
          <button
            type="submit"
            :disabled="isLoading || formData.password !== formData.confirmPassword || formData.password.length < 6"
            class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center"
          >
            <span v-if="!isLoading">Crear Cuenta</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Registrando...
            </span>
          </button>
        </form>

        <!-- Separador -->
        <div class="my-6 flex items-center">
          <div class="flex-1 border-t border-gray-300"></div>
          <div class="px-4 text-gray-600 text-sm">o</div>
          <div class="flex-1 border-t border-gray-300"></div>
        </div>

        <!-- Link a Login -->
        <p class="text-center text-gray-600 text-sm">
          ¿Ya tienes cuenta?
          <router-link
            to="/login"
            class="text-blue-600 hover:text-blue-700 font-medium transition"
          >
            Inicia sesión aquí
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
  nombre: '',
  correo: '',
  password: '',
  confirmPassword: ''
});

const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleRegister = async () => {
  // Limpiar mensajes
  errorMessage.value = '';
  successMessage.value = '';

  // Validar campos
  if (!formData.value.nombre || !formData.value.correo || !formData.value.password) {
    errorMessage.value = 'Por favor completa todos los campos';
    return;
  }

  // Validar que las contraseñas coincidan
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = 'Las contraseñas no coinciden';
    return;
  }

  // Validar largo de contraseña
  if (formData.value.password.length < 6) {
    errorMessage.value = 'La contraseña debe tener al menos 6 caracteres';
    return;
  }

  isLoading.value = true;

  try {
    const result = await authService.register(
      formData.value.nombre,
      formData.value.correo,
      formData.value.password
    );

    if (result.success) {
      successMessage.value = 'Registro exitoso, redirigiendo...';
      
      // Redirigir a la página principal después de 1.5 segundos
      setTimeout(() => {
        router.push('/');
      }, 1500);
    } else {
      errorMessage.value = result.message || 'Error al registrarse';
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
