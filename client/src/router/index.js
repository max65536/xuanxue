import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Ping from '../components/Ping.vue'
import Books from '../components/Books.vue'
import Fus from '../components/Fus.vue'
import Tests from '../components/Test.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'fus',
      component: Fus
    },  
    {
      path: '/book',
      name: 'book',
      component: Books
    },
    {
      path: '/test',
      name: 'test',
      component: Tests
    },    
    {
      path: '/ping',
      name: 'ping',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Ping
    }   
  ]
})

export default router
