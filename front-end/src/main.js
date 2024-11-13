import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import { authAxios, publicAxios } from './axios' // authAxios와 publicAxios로 명시적 import

import '@/assets/normalize.css'
import '@/assets/base.css'
import '@/assets/font.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 새로고침 시 스크롤을 최상단으로 고정하고, localStorage의 'movies_loaded' 값을 제거하여 초기화
window.addEventListener('beforeunload', () => {
  localStorage.removeItem('movies_loaded')
  window.scrollTo(0, 0)
})

app.use(pinia)
app.use(router)
app.mount('#app')

// Axios 인스턴스를 전역에 추가
app.config.globalProperties.$authAxios = authAxios
app.config.globalProperties.$publicAxios = publicAxios
