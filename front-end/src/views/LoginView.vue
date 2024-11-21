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
import { ref } from 'vue'
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
  const REDIRECT_URI = 'http://127.0.0.1:5173/kakao/login'
  const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`
  window.location.href = KAKAO_AUTH_URL
}



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
