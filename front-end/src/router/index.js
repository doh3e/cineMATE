import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import HomeView from '../views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import MypageView from '@/views/MypageView.vue'
import MovieSearchView from '@/views/MovieSearchView.vue'
import MovieforyouView from '@/views/MovieforyouView.vue'
import ReviewView from '@/views/ReviewView.vue'
import MovieCurationView from '@/views/MovieCurationView.vue'
import MovieByGenreView from '@/views/MovieByGenreView.vue'
import FirstTimeView from '@/views/FirstTimeView.vue'


const routes = [
  {
    path: '/first-time',
    name: 'FirstTime',
    component: FirstTimeView,
  },
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
    path: '/mypage/:username',
    name: 'Mypage',
    component: MypageView,
  },
  {
    path: '/search',
    name: 'Search',
    component: MovieSearchView,
  },
  {
    path: '/movie',
    name: 'Movie',
    component: MovieByGenreView,
  },
  {
    path: '/curation',
    name: 'MovieCuration',
    component: MovieCurationView,
  },
  {
    path: '/review',
    name: 'Review',
    component: ReviewView,
    redirect: { name: 'ReviewList' },
    children: [
      {
        path: '',
        name: 'ReviewList',
        component: () => import('@/components/community/ReviewList.vue'),
      },
      {
        path: 'write',
        name: 'ReviewWrite',
        component: () => import('@/components/community/ReviewWrite.vue'),
      }, 
      {
        path: ':review_id',
        name: 'ReviewDetail',
        component: () => import('@/components/community/ReviewDetail.vue'),
      }, 
    ]
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
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const store = useCounterStore()

  const isAuthenticated = store.userInfo && store.userInfo.id

  if ((to.name === 'Login' || to.name === 'SignUp') && isAuthenticated) {
    alert('이미 로그인 되어 있습니다!')
    next({ name: 'Home' })
  }
  else if ((to.name === 'Mypage' || to.name === 'MovieCuration' ||
    to.name === 'Review' || to.name === 'ReviewList' || to.name === 'ReviewWrite' ||
    to.name === 'ReviewDetail' || to.name === 'Movieforyou'
  ) && !isAuthenticated) {
    alert('로그인 한 사용자만 이용할 수 있습니다!')
    next({ name: 'Login' })
  }
  else {
    next()
  }
})


export default router
