import { ref } from 'vue'
import { defineStore } from 'pinia'
import { authAxios, publicAxios } from '@/axios'

export const useCounterStore = defineStore('counter', () => {
  const top_movies = ref([])
  const currentPage = ref(1)
  const hasMore = ref(true)
  const userInfo = ref(null)
  const authToken = ref(localStorage.getItem('authToken') || null)

  const resetPagination = () => {
    top_movies.value = []
    currentPage.value = 1
    hasMore.value = true
  }

  const loadMovies = async () => {
    if (!hasMore.value) return
    try {
      const response = await publicAxios.get(`/movies/?page=${currentPage.value}`)
      top_movies.value.push(...response.data.results)
      currentPage.value += 1
      hasMore.value = response.data.next !== null
    } catch (error) {
      console.error('페이지네이션 데이터 로드 중 오류 발생:', error)
    }
  }

  const getUserInfo = async () => {
    try {
      if (authToken.value) {
        const response = await authAxios.get('/accounts/dj-rest-auth/user/')
        userInfo.value = response.data
      } else {
        console.error("로그인 토큰이 없습니다.")
      }
    } catch (error) {
      console.error('유저 정보를 가져오는 중 오류 발생:', error)
    }
  }

  const login = async (username, password) => {
    try {
      const response = await publicAxios.post('/accounts/dj-rest-auth/login/', {
        username,
        password,
      })

      authToken.value = response.data.access // 응답에서 access 토큰을 받아옴
      localStorage.setItem('authToken', authToken.value)

      // 로그인 후 유저 정보를 가져옴
      await getUserInfo()
    } catch (error) {
      console.error('로그인 실패:', error)
    }
  }

  const logout = async () => {
    try {
      await authAxios.post('/accounts/dj-rest-auth/logout/')
      authToken.value = null
      userInfo.value = null
      localStorage.removeItem('authToken')
    } catch (error) {
      console.error('로그아웃 실패:', error)
    }
  }

  return {
    top_movies,
    currentPage,
    hasMore,
    userInfo,
    resetPagination,
    loadMovies,
    getUserInfo,
    login,
    logout,
  }
}, { persist: true })
