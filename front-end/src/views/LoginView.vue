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
    <button>아이디찾기</button><button>비밀번호찾기</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { publicAxios } from '@/axios';

const store = useCounterStore()
const router = useRouter()

// 폼 데이터와 에러 메시지
const form = ref({
  username: '',
  password: '',
})
const errorMessage = ref('')

// 로그인 처리 함수
const handleLogin = async () => {
  try {
    await store.login(form.value.username, form.value.password)
  } catch (error) {
    errorMessage.value = '로그인 실패. 다시 시도해주세요.'
  }
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
