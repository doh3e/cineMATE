import axios from 'axios'

const authAxios = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
})

authAxios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')  // 여기서 localStorage에서 직접 가져옵니다.
  if (token) {
    config.headers['Authorization'] = `Token ${token}`
  }
  return config
})

const publicAxios = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
})

export { authAxios, publicAxios }
