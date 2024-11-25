<template>
  <div class="user-edit-container">
    <h2 class="edit-title">회원수정</h2>
    <form @submit.prevent="submitForm" class="edit-form">
      <div class="text-form">
        <input type="text" v-model="form.nickname" id="nickname" placeholder="닉네임" />
      </div>
      <p v-if="errors.nickname" class="error">{{ errors.nickname }}</p>

      <div class="text-form">
        <input type="password" v-model="form.old_password" placeholder="현재비밀번호" id="old_password" required />
      </div>
      <p v-if="!form.old_password" class="error">현재 비밀번호는 필수입니다.</p>
      <div class="text-form">
        <input type="password" v-model="form.new_password1" placeholder="새 비밀번호" id="new_password1" />
      </div>
      <p v-if="errors.new_password1" class="error">{{ errors.new_password1 }}</p>
      <div class="text-form">
        <input type="password" v-model="form.new_password2" placeholder="새 비밀번호 확인" id="new_password2" />
      </div>
      <p v-if="errors.new_password2" class="error">{{ errors.new_password2 }}</p>
      <div class="text-form">
        <input type="email" v-model="form.email" id="email" placeholder="이메일" required />
      </div>
      <p v-if="errors.email" class="error">{{ errors.email }}</p>

      <h3>선택사항</h3>

      <div class="date-form">
        <label for="birthday">생년월일</label>
        <input v-model="form.birthday" type="date" id="birthday" />
      </div>
      <p v-if="errors.birthday" class="error">{{ errors.birthday }}</p>
      <div class="image-form">
        <label for="profile-image">프로필사진</label>
        <div v-if="previewImage" class="upload-display">
          <div class="upload-thumb-wrap">
            <img :src="previewImage" alt="미리보기 이미지" class="upload-thumb" />
          </div>
        </div>
        <div class="filebox preview-image">
          <input class="upload-name" :value="fileName" disabled="disabled" >
          <label for="input-file">업로드</label> 
          <input @change="handleImageUpload" type="file" id="input-file" class="upload-hidden"> 
        </div>
      </div>
      <div class="form-button">
        <button type="submit" :disabled="!isFormValid" class="btn submit-btn">수정</button>
      </div>
    </form>
    <button @click="goodbye">회원탈퇴</button>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref, watch, computed } from 'vue'
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
  birthday: null,
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
  if (!form.new_password1) {
    errors.new_password1 = ''
  } else {
    errors.new_password1 = validatePassword(form.new_password1)
  }
})

watch(() => form.new_password2, () => {
  if (!form.new_password2) {
    errors.new_password2 = ''
  } else {
    errors.new_password2 = validatePasswordMatch(form.new_password1, form.new_password2)
  }
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

onMounted(() => {
  if (store.userInfo) {
    form.email = store.userInfo.email || ''
    form.nickname = store.userInfo.nickname || ''
    form.birthday = store.userInfo.birthday || ''
  }
})

const fileName = ref('파일선택')
const previewImage = ref(null) 

// 프로필사진 업로드 처리 함수
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.match('image.*')) {
      alert('이미지 파일만 업로드할 수 있습니다.')
      return
    }
    fileName.value = file.name
    form.profile_image = file

    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target.result
    }
    reader.readAsDataURL(file)

  } else {
    fileName.value = '파일선택'
    form.profile_image = null
    previewImage.value = null
  }
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

* {
  margin: 0px;
  padding: 0px;
  text-decoration: none;
}

.user-edit-container {
  max-width: 400px;
  height: 90%;
  margin: 0 auto;
  gap: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  overflow-y: hidden;
}

.edit-title {
  font-family: 'S-CoreDream';
  font-weight: 600;
  font-size: 2rem;
  margin-bottom: 20px;
  text-align: center;
}

.edit-form {
  width: 100%;
  height: 600px;
  overflow-y: scroll !important;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 15px;
}

.text-form {
  border-bottom: 2px solid #adadad;
  margin: 0 20px;
  padding: 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.date-form, .image-form {
  width: 100%;
  margin: 10px 30px;
  padding: 10px 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.date-form > label,
.image-form > label {
  width: 50%;
  height: auto;
  text-align:center;
  color: #1f1f1f;
  padding-bottom: 10px;
  border-bottom: 2px solid #adadad;
}

#birthday {
  border-radius: 5px;
  width: 60%;
  padding: 5px;
  opacity: 0.8;
}

.filebox input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip:rect(0,0,0,0);
  border: 0;
}

.filebox label {
  display: inline-block;
  padding: 5px;
  color: #f8f8f8;
  font-size: 0.9rem;
  line-height: normal;
  vertical-align: middle;
  background-color: #AD88C6;
  cursor: pointer;
  border-radius: .25em;
}

.filebox .upload-name {
  display: inline-block;
  padding: 5px;
  font-size: 0.8rem;
  font-family: inherit;
  line-height: normal;
  vertical-align: middle;
  background-color: #f5f5f5;
  border: 1px solid #ebebeb;
  border-bottom-color: #e2e2e2;
  border-radius: 5px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.upload-display {
  margin-bottom: 5px;
}

@media(min-width: 768px) { 
  .upload-display {
    display: inline-block;
    margin-right: 5px;
    margin-bottom: 0;
  }
}

.upload-thumb-wrap {
  display: inline-block;
  width: 100px;
  padding: 2px;
  vertical-align: middle;
  border-radius: 5px;
}

.upload-display img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: cover;
}

#nickname {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

#email {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

#old_password, #new_password1, #new_password2 {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

.form-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100px;
}

.submit-btn {
  position:relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  width:60%;
  height:40px;
  background: linear-gradient(125deg,#7469B6,#E1afd1,#AD88C6);
  background-position: left;
  background-size: 200%;
  color:white;
  font-weight: bold;
  border:none;
  cursor:pointer;
  transition: 0.4s;
  display:inline;
}

.submit-btn:hover {
  background-position: right;
}

.submit-btn:disabled {
  background: #cccccc;
  color: #666666;
  cursor: not-allowed;
  background-size: 100%;
  transition: none;
}

.error {
  color: red;
  font-size: 0.8em;
  text-align: center;
}

</style>
