<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignUp">
      <div>
        <label for="username">Username</label>
        <input v-model="form.username" type="text" id="username" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input v-model="form.email" type="email" id="email" required />
      </div>
      <div>
        <label for="password1">Password</label>
        <input v-model="form.password1" type="password" id="password1" required />
      </div>
      <div>
        <label for="password2">Confirm Password</label>
        <input v-model="form.password2" type="password" id="password2" required />
      </div>
      <div>
        <label for="nickname">Nickname</label>
        <input v-model="form.nickname" type="text" id="nickname" required />
      </div>
      <div>
        <label for="birthday">Birthday</label>
        <input v-model="form.birthday" type="date" id="birthday" required />
      </div>
      <div>
        <label for="profileImage">Profile Image</label>
        <input @change="handleImageUpload" type="file" id="profileImage" />
      </div>
      <button type="submit">회원가입</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { authAxios, publicAxios } from '@/axios'

export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        password1: '',
        password2: '',
        nickname: '',
        birthday: null,
        profile_image: null,
      },
      errorMessage: '',
    }
  },
  methods: {
    handleImageUpload(event) {
      this.form.profile_image = event.target.files[0]
    },
    async handleSignUp() {
      const formData = new FormData()
      for (const key in this.form) {
        formData.append(key, this.form[key])
      }

      formData.forEach((value, key) => {
        console.log(`${key}: ${value}`)
      })

      try {
        const response = await publicAxios.post('/accounts/dj-rest-auth/registration/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        if (response.status === 201) {
          const token = response.data.key
          localStorage.setItem('authToken', token)

          this.$router.push({ path: '/' })
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || '회원가입 실패. 다시 시도해주세요.'
        console.error("회원가입 오류:", error.response?.data)
      }
    },
  },
}

</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: auto;
}
.error {
  color: red;
}
</style>
