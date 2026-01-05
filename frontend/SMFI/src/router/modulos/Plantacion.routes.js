import Grafico from '@/views/plantacion/Grafico.vue'
import ListaPlantaciones from '@/views/plantacion/ListaPlantaciones.vue'
import Plantacion from '@/views/plantacion/Plantacion.vue'
import MonitoreoPlantacion from '@/views/plantacion/MonitoreoPlantacion.vue'

export default [
  {
    path: '/plantacion/grafico',
    name: 'Grafico',
    component: Grafico,
    meta: { layout: 'default' }
  },

  {
    path : '/plantacion/lista',
    name : 'ListaPlantaciones',
    component : ListaPlantaciones,
    meta: { layout: 'default' }
  },
  {
    path : '/plantacion/:id',
    name : 'Plantacion',
    component : Plantacion,
    meta: { layout: 'default' }
  },
  {
    path : '/plantacion/monitoreo',
    name : 'MonitoreoPlantacion',
    component : MonitoreoPlantacion,
    meta: { layout: 'default' }
  }

]