import axios from 'axios';

// En desarrollo: usar el proxy de vite (/api apunta a https://localhost:8000/api)
// En producción: usar la URL real de la API
const API_URL = import.meta.env.PROD 
  ? 'https://api.ejemplo.com/api'  // Cambiar en producción
  : '/api';  // Usa proxy en desarrollo

// Crear instancia de axios con configuración base
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  /**
   * Registra un nuevo usuario
   * @param {string} nombre - Nombre del usuario
   * @param {string} correo - Email único
   * @param {string} password - Contraseña
   * @param {number} rol_id - ID del rol (opcional)
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async register(nombre, correo, password, rol_id = null) {
    try {
      const response = await apiClient.post('/register/', {
        nombre,
        correo,
        password,
        rol_id
      });
      
      if (response.data.success) {
        // Guardar usuario en localStorage
        localStorage.setItem('usuario', JSON.stringify(response.data.usuario));
        localStorage.setItem('token', response.data.usuario.id);
      }
      
      return response.data;
    } catch (error) {
      console.error('Error en registro:', error);
      return {
        success: false,
        message: error.response?.data?.message || 'Error al registrar usuario'
      };
    }
  },

  /**
   * Autentica un usuario existente
   * @param {string} correo - Email del usuario
   * @param {string} password - Contraseña
   * @returns {Promise<Object>} Respuesta del servidor con usuario autenticado
   */
  async login(correo, password) {
    try {
      const response = await apiClient.post('/login/', {
        correo,
        password
      });
      
      if (response.data.success) {
        // Guardar usuario y token en localStorage
        localStorage.setItem('usuario', JSON.stringify(response.data.usuario));
        localStorage.setItem('token', response.data.usuario.id);
        localStorage.setItem('userRole', response.data.usuario.rol || 'user');
      }
      
      return response.data;
    } catch (error) {
      console.error('Error en login:', error);
      return {
        success: false,
        message: error.response?.data?.message || 'Error al iniciar sesión'
      };
    }
  },

  /**
   * Cierra la sesión del usuario
   */
  logout() {
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
  },

  /**
   * Obtiene el usuario actualmente autenticado
   * @returns {Object|null} Objeto usuario o null si no hay sesión
   */
  getCurrentUser() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? JSON.parse(usuario) : null;
  },

  /**
   * Verifica si el usuario está autenticado
   * @returns {boolean} True si hay usuario en sesión
   */
  isAuthenticated() {
    return !!localStorage.getItem('token');
  },

  /**
   * Obtiene el token de autenticación
   * @returns {string|null} Token o null
   */
  getToken() {
    return localStorage.getItem('token');
  },

  /**
   * Cambia la contraseña del usuario
   * @param {number} usuario_id - ID del usuario
   * @param {string} old_password - Contraseña actual
   * @param {string} new_password - Nueva contraseña
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async changePassword(usuario_id, old_password, new_password) {
    try {
      const response = await apiClient.post('/change-password/', {
        usuario_id,
        old_password,
        new_password
      });
      return response.data;
    } catch (error) {
      console.error('Error al cambiar contraseña:', error);
      return {
        success: false,
        message: error.response?.data?.message || 'Error al cambiar contraseña'
      };
    }
  }
};
