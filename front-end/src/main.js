import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import axios from './axios'

import '@/assets/normalize.css';
import '@/assets/base.css';
import '@/assets/font.css';


const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.config.globalProperties.$axios = axios

app.use(pinia)
app.use(router)
app.mount('#app')
