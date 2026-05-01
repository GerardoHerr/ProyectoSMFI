import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'

export default [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/registro',
    name: 'Registro',
    component: Registro,
    meta: { layout: 'auth', requiresAuth: false }
  }
]
