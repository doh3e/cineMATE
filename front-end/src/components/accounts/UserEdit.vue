<template>
  <div class="user-edit-container">
    <h2>회원 정보 수정</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="nickname">닉네임</label>
        <input type="text" v-model="form.nickname" id="nickname" required />
        <p v-if="errors.nickname" class="error-message">{{ errors.nickname }}</p>
      </div>
      <div>
        <label for="old_password">현재 비밀번호</label>
        <input type="password" v-model="form.old_password" id="old_password" required />
        <p v-if="!form.old_password" class="error-message">현재 비밀번호는 필수입니다.</p>
      </div>
      <div>
        <label for="new_password1">새 비밀번호</label>
        <input type="password" v-model="form.new_password1" id="new_password1" />
        <p v-if="errors.new_password1" class="error-message">{{ errors.new_password1 }}</p>
      </div>
      <div>
        <label for="new_password2">새 비밀번호 확인</label>
        <input type="password" v-model="form.new_password2" id="new_password2" />
        <p v-if="errors.new_password2" class="error-message">{{ errors.new_password2 }}</p>
      </div>
      <div>
        <label for="email">이메일</label>
        <input type="email" v-model="form.email" id="email" required />
        <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
      </div>
      <div>
        <label for="birthday">생일</label>
        <input type="date" v-model="form.birthday" id="birthday" />
        <p v-if="errors.birthday" class="error-message">{{ errors.birthday }}</p>
      </div>
      <div>
        <label for="profile_image">프로필 이미지</label>
        <input type="file" @change="handleFileChange" id="profile_image" />
      </div>
      <button type="submit" :disabled="!isFormValid">저장</button>
    </form>
    <button @click="goodbye">회원탈퇴</button>
  </div>
</template>

<script setup>
import { reactive, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter'
import {
  validateEmail,
  validatePassword,
  validatePasswordMatch,
  validateNickname,
  validateBirthday,
} from '@/utils/validators'

const router = useRouter()
const route = useRoute()
const store = useCounterStore()

const form = reactive({
  email: '',
  nickname: '',
  birthday: '',
  profile_image: null,
  old_password: '',
  new_password1: '',
  new_password2: '',
})

const errors = reactive({
  email: '',
  nickname: '',
  birthday: '',
  old_password: '',
  new_password1: '',
  new_password2: '',
})

watch(() => form.email, () => {
  errors.email = validateEmail(form.email)
})

watch(() => form.new_password1, () => {
  errors.new_password1 = validatePassword(form.new_password1)
})

watch(() => form.new_password2, () => {
  errors.new_password2 = validatePasswordMatch(form.new_password1, form.new_password2)
})

watch(() => form.nickname, () => {
  errors.nickname = validateNickname(form.nickname)
})

watch(() => form.birthday, () => {
  errors.birthday = validateBirthday(form.birthday)
})

const isFormValid = computed(() => {
  return (
    !errors.email &&
    !errors.nickname &&
    !errors.birthday &&
    !errors.new_password1 &&
    !errors.new_password2 &&
    form.old_password // 필수
  )
})


// store에서 초기값 가져오기
onMounted(() => {
  if (store.userInfo) {
    form.email = store.userInfo.email || ''
    form.nickname = store.userInfo.nickname || ''
    form.birthday = store.userInfo.birthday || ''
  }
})

// 파일 선택 핸들러
const handleFileChange = (event) => {
  const file = event.target.files[0]
  form.profile_image = file
}

// 회원 탈퇴
const goodbye = async () => {
  if(route.params.username !== store.userInfo.username) {
    alert('탈퇴 권한이 없습니다!')
    return
  }
  const isReal = confirm('정말 회원 탈퇴를 하시겠어요?')
  if(isReal){
    try{
      await authAxios.delete(`/accounts/delete/${store.userInfo.id}`)
      alert('정상적으로 탈퇴 되었습니다.')
      store.logout()
    }
    catch(error) {
      console.error('회원 탈퇴 오류:', error.response?.data || error.message)
      alert('회원 탈퇴에 실패했습니다. 잠시 후 다시 시도해주세요.')   
    }
  }
}

// 회원 수정
const submitForm = async () => {
  if(route.params.username !== store.userInfo.username) {
    alert('수정 권한이 없습니다!')
    return
  }
  try {
    const formData = new FormData()
    for (const key in form) {
      if (form[key] !== null && form[key] !== '') {
        formData.append(key, form[key])
      }
    }

    await authAxios.patch('/accounts/dj-rest-auth/user/', formData)
    alert('회원 정보가 수정되었습니다.')

    // 사용자 정보 업데이트
    await store.getUserInfo()
    window.location.reload()
  } catch (error) {
    console.error('회원 정보 수정 오류:', error.response?.data || error.message)
    alert('회원 정보 수정에 실패했습니다. 입력 내용을 확인해주세요.')
  }
}
</script>

<style scoped>
.user-edit-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}
form div {
  margin-bottom: 15px;
}
button {
  display: block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
.error-message {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}
</style>
