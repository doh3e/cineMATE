import { ref } from 'vue'
import { defineStore } from 'pinia'
import { authAxios, publicAxios } from '@/axios'


export const useCounterStore = defineStore('counter', () => {
  const top_movies = ref([])  // 영화 데이터
  const currentPage = ref(1)  // 페이지
  const hasMore = ref(true)  // 추가 데이터 유무
  const userInfo = ref(null)  // 사용자 정보
  const authToken = ref(localStorage.getItem('authToken') || null)  // 토큰

  const resetPagination = () => {
    top_movies.value = []
    currentPage.value = 1
    hasMore.value = true
  }

  // top_movies에 데이터가 없을 시 (최초로드가 안되어있을 시) 영화 데이터 로드
  const loadMovies = async () => {
    if (top_movies.value.length === 0) {
      await loadTopRatedMoviesFromAPI()
    }

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

  // API에서 영화 데이터 가져오기
  const loadTopRatedMoviesFromAPI = async () => {
    try {
      const response = await publicAxios.get('/movies/load-top-list/')
      if (response.data.success) {
        console.log('영화 데이터가 API에서 로드되었습니다.')
      }
    } catch (error) {
      console.error('API에서 영화 데이터를 로드하는 중 오류 발생:', error)
    }
  }

  const getUserInfo = async () => {
    try {
      const token = localStorage.getItem('authToken')
      if (token) {
        const response = await authAxios.get('/accounts/dj-rest-auth/user/') // authAxios 사용, 헤더에 자동으로 JWT 포함
        userInfo.value = response.data
      } else {
        console.error('로그인 토큰이 없습니다.')
      }
    } catch (error) {
      console.error('유저 정보를 가져오는 중 오류 발생:', error)
    }
  }
  

  // 로그인
  const login = async (username, password) => {
    try {
      // JWT 토큰 발급하기
      const response = await publicAxios.post('accounts/api/token/', {
        username,
        password
      })

      // 받아온 토큰을 로컬 스토리지에 저장
      const token = response.data.access
      localStorage.setItem('authToken', token)
  
      await getUserInfo()
      if(userInfo.value){
        alert(`${userInfo.value.username}님, 어서오세요!`)
      }
    } catch (error) {
      console.error('로그인 실패:', error)
    }
  }

  // 로그아웃
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
