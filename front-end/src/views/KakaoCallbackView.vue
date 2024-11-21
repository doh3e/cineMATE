<template>
  <div>로그인 처리 중...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter';
import { publicAxios } from '@/axios'

const router = useRouter()
const store = useCounterStore()

onMounted(async () => {
  console.log('KakaoCallbackView mounted')
  const urlParams = new URLSearchParams(window.location.search)
  const authCode = urlParams.get('code')
  console.log(authCode)

  if (!authCode) {
    console.error('Authorization code is missing.')
    return
  }

  try {
    const response = await publicAxios.get('/accounts/kakao/login/callback/', {
      params: { code: authCode },
    })

    const { access_token, refresh_token } = response.data

    // 토큰 저장
    localStorage.setItem('authToken', access_token)
    localStorage.setItem('refreshToken', refresh_token)

    // 사용자 상태 업데이트
    console.log('User Info:', user)
    store.getUserInfo()
    router.replace({ name: 'Home' }) // Home 페이지로 이동
  } catch (error) {
    console.error('Failed to fetch tokens:', error.response?.data || error.message)
  }
})
</script>
