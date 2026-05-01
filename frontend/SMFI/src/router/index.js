import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'

import AuthRoutes from './modulos/Auth.routes.js'
import UsuarioRoutes from './modulos/Usuario.routes.js'
import PlantacionRoutes from './modulos/Plantacion.routes.js'


const routes = [
    ...AuthRoutes,
    ...UsuarioRoutes,
    ...PlantacionRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard para proteger rutas autenticadas
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()
  
  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth !== false && !isAuthenticated) {
    // Si está en una ruta pública (login/registro), permitir acceso
    if (to.path === '/login' || to.path === '/registro') {
      next()
    } else {
      // Redirigir a login si no está autenticado
      next('/login')
    }
  } else {
    // Si está autenticado e intenta acceder a login/registro, redirigir a inicio
    if (isAuthenticated && (to.path === '/login' || to.path === '/registro')) {
      next('/')
    } else {
      next()
    }
  }
})

export default router
