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
  </div>
</template>

<script>
import { useCounterStore } from '@/stores/counter'

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      errorMessage: '',
    }
  },
  methods: {
    async handleLogin() {
      const store = useCounterStore()
      try {
        await store.login(this.form.username, this.form.password)
        this.$router.push({ path: '/' })
      } catch (error) {
        console.error('로그인 오류:', error)
        this.errorMessage = '로그인 실패. 다시 시도해주세요.'
      }
    },
  },
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
