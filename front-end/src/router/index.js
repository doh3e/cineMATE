import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUpView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }  // 항상 스크롤을 최상단으로 이동
  }
})

export default router
