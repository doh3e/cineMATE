<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username</label>
        <input v-model="form.username" type="text" id="username" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input v-model="form.password" type="password" id="password" required />
      </div>
      <button type="submit">로그인</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <button @click="loginWithKakao">카카오로 로그인</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { publicAxios } from '@/axios';

const KAKAO_REST_ID = import.meta.env.VITE_KAKAO_REST_ID
console.log(KAKAO_REST_ID)

const store = useCounterStore()
const router = useRouter()

// 폼 데이터와 에러 메시지
const form = ref({
  username: '',
  password: '',
})
const errorMessage = ref('')

// 로그인 처리 함수
const loginWithKakao = async () => {
  const REDIRECT_URI = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
  const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`
  window.location.href = KAKAO_AUTH_URL
}

// 카카오 콜백 처리 함수
const processKakaoCallback = async () => {
  const codeParams = new URLSearchParams(window.location.search)
  const authCode = codeParams.get('code')

  if (!authCode) {
    console.error('Authorization code is missing.')
    return
  }

  try {
    // 백엔드로 인가 코드 전달 (POST 요청)
    const response = await publicAxios.post('/accounts/kakao/login/callback/', {
      code: authCode,
    })

    const { access_token, refresh_token } = response.data

    // JWT 저장
    localStorage.setItem('authToken', access_token)
    localStorage.setItem('refreshToken', refresh_token)

    console.log('JWT 토큰 저장 완료!')

    // 사용자 상태 업데이트
    await store.getUserInfo()

    // URL 정리
    router.replace({ name: 'Home' }) // 홈 페이지로 리다이렉트
  } catch (error) {
    console.error('로그인 처리 실패:', error.response?.data || error.message)
    alert('로그인에 실패했습니다. 다시 시도해주세요.')
  }
}

// 페이지가 로드되었을 때 카카오 콜백 처리
onMounted(() => {
  processKakaoCallback()
})

</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
}
.error {
  color: red;
}
</style>
