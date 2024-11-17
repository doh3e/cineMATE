import { ref } from 'vue'
import { defineStore } from 'pinia'
import { authAxios, publicAxios } from '@/axios'
import { useRouter } from 'vue-router'


export const useCounterStore = defineStore('counter', () => {

  const router = useRouter()
  
  const GENRE_MAP = {
    28: "액션",
    12: "어드벤처",
    16: "애니메이션",
    35: "코미디",
    80: "범죄",
    99: "다큐멘터리",
    18: "드라마",
    10751: "가족",
    14: "판타지",
    36: "역사",
    27: "공포",
    10402: "음악",
    9648: "미스터리",
    10749: "로맨스",
    878: "SF",
    10770: "TV 영화",
    53: "스릴러",
    10752: "전쟁",
    37: "서부"
  }

  const getGenreNameById = (id) => {
    return GENRE_MAP[id] || "알 수 없음"
  }

  const topMovies = ref([])

  const loadTopMovies = async () => {
    if (topMovies.value.length === 0) {
      try {
        const response = await publicAxios.get('/movies/')
        if (response.data.length > 0) {
          topMovies.value = response.data
          console.log('DB에서 영화 데이터를 성공적으로 로드했습니다.')
        } else {
          console.log('DB에 영화 데이터가 없어 TMDB API에서 로드합니다.')
          const tmdbResponse = await publicAxios.get('/movies/load-top-list/')
          if (tmdbResponse.data.success) {
            console.log('TMDB API에서 데이터를 성공적으로 가져왔습니다. DB에서 데이터를 다시 로드합니다.')
            const dbResponse = await publicAxios.get('/movies/')
            topMovies.value = dbResponse.data
          } else {
            console.error('TMDB API에서 데이터를 가져오는 데 실패했습니다.')
          }
        }
      } catch (error) {
        console.error('영화 데이터를 로드하는 중 오류 발생:', error)
      }
    }
  }

  const userInfo = ref(null) // 사용자 정보
  const authToken = ref(localStorage.getItem('authToken') || null) // 토큰

  const getUserInfo = async () => {
    try {
      const token = localStorage.getItem('authToken')
      if (token) {
        const response = await authAxios.get('/accounts/dj-rest-auth/user/')
        userInfo.value = response.data
      } else {
        console.error('로그인 토큰이 없습니다.')
      }
    } catch (error) {
      console.error('유저 정보를 가져오는 중 오류 발생:', error)
    }
  }

  const login = async (username, password) => {
    try {
      const response = await publicAxios.post('accounts/api/token/', {
        username,
        password
      })

      const token = response.data.access
      localStorage.setItem('authToken', token)

      await getUserInfo()
      if (userInfo.value) {
        alert(`${userInfo.value.nickname}님, 어서오세요!`)
      }
    } catch (error) {
      alert('아이디 혹은 비밀번호를 다시 확인해주세요!')
    }
  }

  const logout = async () => {
    try {
      await authAxios.post('/accounts/dj-rest-auth/logout/')
      authToken.value = null
      userInfo.value = null
      localStorage.removeItem('authToken')
      alert('로그아웃 되었습니다!')
      router.replace('/')
    } catch (error) {
      console.error('로그아웃 실패:', error)
    }
  }

  const getImageUrl = (path) => {
    return `https://image.tmdb.org/t/p/w500${path}`
  }

  return {
    GENRE_MAP,
    getGenreNameById,
    topMovies,
    loadTopMovies,
    userInfo,
    getUserInfo,
    login,
    logout,
    getImageUrl
  }
}, { persist: true })
