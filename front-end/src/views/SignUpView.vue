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

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { publicAxios } from '@/axios'

// 데이터 정의
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  birthday: null,
  profile_image: null,
})

const errorMessage = ref('')

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  form.profile_image = event.target.files[0]
}

// 회원가입 처리
const handleSignUp = async () => {
  const formData = new FormData()
  for (const key in form) {
    formData.append(key, form[key])
  }

  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`) // 디버깅용 출력
  })

  try {
    const response = await publicAxios.post('/accounts/dj-rest-auth/registration/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    if (response.status === 201) {
      const token = response.data.key
      localStorage.setItem('authToken', token)
      alert('회원가입을 환영합니다!')
      router.push('/') // 홈으로 이동
      window.location.reload() // 새로고침으로 상태 초기화
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '회원가입 실패. 다시 시도해주세요.'
    console.error('회원가입 오류:', error.response?.data)
  }
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
