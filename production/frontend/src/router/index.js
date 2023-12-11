import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/about',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/',
    name: 'user',
    component: () => import( '../layout/MainLayoutChat.vue'),
    redirect:"/home",
    children:
    [
      {
        path: '/home',
        name: 'home',
        component: HomeView
      },
      {
        path: '/calendar',
        name: 'calendar',
        component: () => import(/* webpackChunkName: "about" */ '../views/CalendarView.vue')
      },
      
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import(/* webpackChunkName: "about" */ '../views/DashBoardView.vue')
      },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
