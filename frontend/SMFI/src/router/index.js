import { createRouter, createWebHistory } from 'vue-router'

import UsuarioRoutes from './modulos/Usuario.routes.js'
import PlantacionRoutes from './modulos/Plantacion.routes.js'


const routes = [
    ...UsuarioRoutes,
    ...PlantacionRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
