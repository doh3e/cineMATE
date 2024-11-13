import axios from 'axios'

const authAxios = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
})

authAxios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
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
