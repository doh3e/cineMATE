import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import HomeView from '../views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MypageView from '@/views/MypageView.vue'
import RecommendView from '@/views/RecommendView.vue'
import MovieforyouView from '@/views/MovieforyouView.vue'

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
  {
    path: '/mypage',
    name: 'Mypage',
    component: MypageView,
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: RecommendView,
  },
  {
    path: '/movieforyou',
    name: 'Movieforyou',
    component: MovieforyouView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }  // 항상 스크롤을 최상단으로 이동
  }
})

router.beforeEach((to, from, next) => {
  const store = useCounterStore()

  const isAuthenticated = store.userInfo && store.userInfo.id

  if ((to.name === 'Login' || to.name === 'SignUp') && isAuthenticated) {
    alert('이미 로그인 되어 있습니다!')
    next({ name: 'Home' })
  }
  else if (to.name === 'Mypage' && !isAuthenticated) {
    alert('로그인 한 사용자만 이용할 수 있습니다!')
    next({ name: 'Login' })
  }
  else {
    next()
  }
})


export default router
