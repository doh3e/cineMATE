<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignUp">
      <div>
        <label for="username">아이디</label>
        <input v-model="form.username" type="text" id="username" required />
        <p v-if="errors.username" class="error">{{ errors.username }}</p>
      </div>
      <div>
        <label for="password1">비밀번호</label>
        <input v-model="form.password1" type="password" id="password1" required />
        <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>
      </div>
      <div>
        <label for="password2">비밀번호 확인</label>
        <input v-model="form.password2" type="password" id="password2" required />
        <p v-if="errors.password2" class="error">{{ errors.password2 }}</p>
      </div>
      <div>
        <label for="email">이메일</label>
        <input v-model="form.email" type="email" id="email" required />
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>
      <div>
        <label for="nickname">닉네임</label>
        <input v-model="form.nickname" type="text" id="nickname" required />
        <p v-if="errors.nickname" class="error">{{ errors.nickname }}</p>
      </div>
      <hr>
      <h3>선택사항</h3>
      <div>
        <label for="birthday">생년월일</label>
        <input v-model="form.birthday" type="date" id="birthday" />
        <p v-if="errors.birthday" class="error">{{ errors.birthday }}</p>
        <p>입력 시 좀 더 개인화된 영화 추천을 받을 수 있어요!</p>
      </div>
      <div>
        <label for="profileImage">프로필사진</label>
        <input @change="handleImageUpload" type="file" id="profileImage" />
      </div>
      <button type="submit" :disabled="!isFormValid">회원가입</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { publicAxios } from '@/axios'
import {
  validateUsername,
  validateEmail,
  validatePassword,
  validatePasswordMatch,
  validateNickname,
  validateBirthday,
} from '@/utils/validators'


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

const errors = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  birthday: '',
})

watch(() => form.username, () => {
  errors.username = validateUsername(form.username)
})

watch(() => form.email, () => {
  errors.email = validateEmail(form.email)
})

watch(() => form.password1, () => {
  errors.password1 = validatePassword(form.password1)
})

watch(() => form.password2, () => {
  errors.password2 = validatePasswordMatch(form.password1, form.password2)
})

watch(() => form.nickname, () => {
  errors.nickname = validateNickname(form.nickname)
})

watch(() => form.birthday, () => {
  errors.birthday = validateBirthday(form.birthday)
})

const isFormValid = computed(() => {
  return Object.values(errors).every((error) => !error) &&
         Object.values(form).every((value) => value !== '')
})

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  form.profile_image = event.target.files[0]
}

// 회원가입 처리
const handleSignUp = async () => {
  const formData = new FormData()
  for (const key in form) {
    if (form[key] !== null && form[key] !== '') {
      formData.append(key, form[key])
    }
  }

  try {
    const response = await publicAxios.post('/accounts/dj-rest-auth/registration/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    if (response.status === 201) {
      const token = response.data.key
      localStorage.setItem('authToken', token)
      alert('회원가입을 환영합니다!')
      router.replace({ name: 'Home' }) // 홈으로 이동
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
  font-size: 0.9em;
  margin-top: 0.5em;
}
</style>
