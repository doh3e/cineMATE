<template>
  <div class="bg-black">
    <img src="@/assets/img/universe.png" alt="universe-img" class="bg-universe"
    @mousemove="handleMouseMove"
    @mouseleave="resetTransform" :style="imageStyle">  
  </div>
  <h1 class="yesteryear-regular h1-cali">Your Movie-verse Begins Here</h1>
  <div class="signup-container"
    @mouseenter="resetTransform"
    @mouseleave="handleMouseMove">
    <form @submit.prevent="handleSignUp" class="signup-form">
      <h2 class="h2-cali yesteryear-regular">SignUp</h2>
      
      <div class="text-form">
        <input v-model="form.username" type="text" id="username" placeholder="아이디" autocomplete="username"/>
        <p v-if="errors.username" class="error">{{ errors.username }}</p>
      </div>
        
      <div class="text-form">
        <input v-model="form.password1" type="password" placeholder="비밀번호" id="password1" required autocomplete="new-password"/>
        <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>
      </div>
      
      <div class="text-form">
        <input v-model="form.password2" type="password" placeholder="비밀번호 확인" id="password2" required autocomplete="new-password"/>
        <p v-if="errors.password2" class="error">{{ errors.password2 }}</p>
      </div>

      <div class="text-form">
        <input v-model="form.email" type="email" id="email" placeholder="이메일" required autocomplete="email"/>
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>

      <div class="text-form">
        <input v-model="form.nickname" type="text" id="nickname" placeholder="닉네임" required autocomplete="nickname"/>
        <p v-if="errors.nickname" class="error">{{ errors.nickname }}</p>
      </div>

      <h3>선택사항</h3>

      <div class="date-form">
        <label for="birthday">생년월일</label>
        <input v-model="form.birthday" type="date" id="birthday" />
        <p v-if="errors.birthday" class="error">{{ errors.birthday }}</p>
      </div>

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
        <button type="submit" :disabled="!isFormValid" class="btn submit-btn">가입하기</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash'
import { publicAxios } from '@/axios'
import {
  validateUsername,
  validateEmail,
  validatePassword,
  validatePasswordMatch,
  validateNickname,
  validateBirthday,
} from '@/utils/validators'


const router = useRouter()
const isIdChecked = ref(false)

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

watch(
  () => form.username,
  debounce(async (newVal) => {
    const validationError = validateUsername(newVal)
    if (validationError) {
      errors.username = validationError
      isIdChecked.value = false
      return
    }

    try {
      const response = await publicAxios.get(`/accounts/checkid/${newVal}/`)
      if (response.data.available) {
        isIdChecked.value = true
        errors.username = ''
      } else {
        isIdChecked.value = false
        errors.username = '이미 사용 중인 아이디입니다.'
      }
    } catch (error) {
      console.error('아이디 중복 체크 오류:', error)
      errors.username = '중복 체크 중 오류가 발생했습니다.'
      isIdChecked.value = false
    }
  }, 300)
)


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
  const hasNoErrors = Object.values(errors).every((error) => !error)
  const isComplete = Object.values(form).every((value) => value !== '')
  return hasNoErrors && isComplete && isIdChecked.value
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

// 회원가입 처리
const handleSignUp = async () => {
  const formData = new FormData()
  for (const key in form) {
    if (form[key] !== null && form[key] !== '') {
      formData.append(key, form[key])
    }
  }

  try {
    console.log(formData)
    const response = await publicAxios.post('/accounts/dj-rest-auth/registration/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    if (response.status === 201) {
      const token = response.data.key
      localStorage.setItem('authToken', token)
      alert('회원가입을 환영합니다!')
      router.replace({ name: 'Home' })
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '회원가입 실패. 다시 시도해주세요.'
    console.error('회원가입 오류:', error.response?.data)
  }
}

// 백그라운드 이미지 움직임 처리
const imageStyle = ref({})

const handleMouseMove = (event) => {
  const { clientX, clientY, currentTarget } = event
  const { width, height, left, top } = currentTarget.getBoundingClientRect()

  const x = (clientX - left - width / 2) / (width / 2)
  const y = (clientY - top - height / 2) / (height / 2)

  const rotateX = y * -5
  const rotateY = x * 2
  const translateZ = Math.sqrt(x * x + y * y) * -3

  imageStyle.value = {
    transform: `perspective(500px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(${translateZ}px)`,
    transition: 'transform 0.6s ease-out',
  }
}

const resetTransform = () => {
  imageStyle.value = {
    transform: 'perspective(500px) rotateX(0deg) rotateY(0deg) translateZ(0px)',
    transition: 'transform 0.5s ease-out',
  }
}

</script>

<style scoped>

* {
  margin: 0px;
  padding: 0px;
  text-decoration: none;
  overflow: hidden;
}

.bg-black {
  position: absolute;
  padding-top: 80px;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
  opacity: 1;
  background-color: #1f1f1f;
  transform-style: preserve-3d;
}

.bg-universe {
  width: 400%;
  height: auto;
  z-index: 2;
  opacity: 0.9;
  will-change: transform;
  transition: transform 0.5s ease-out;
  transform-origin: center;
}

.h1-cali {
  position: absolute;
  top: 40%;
  z-index: 2;
  margin: 0 auto;
  text-align: center;
  vertical-align: middle;
  font-size: 12rem;
  color: #f8f8f8;
  opacity: 0.5;
  pointer-events: none;
}

.signup-container {
  max-width: 400px;
  margin: auto;
}

.signup-form {
  position:absolute;
  width: 400px;
  height: 650px;
  padding: 30px, 20px;
  background-color: rgba(255, 255, 255, 0.7);
  text-align:center;
  z-index: 3;
  top:50%;
  left:50%;
  transform: translate(-50%,-50%);
  border-radius: 15px;
  overflow-y: scroll;
}

.h2-cali {
  text-align: center;
  margin: 30px;
  font-size: 3rem;
}

.text-form {
  border-bottom: 2px solid #adadad;
  margin: 30px;
  padding: 10px 10px;
}

.text-form > p {
  font-size: 0.8rem;
}

.date-form, .image-form {
  margin: 30px;
  padding: 10px 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.date-form > label,
.image-form > label {
  width: 50%;
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

#username {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

#password1, #password2 {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
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

.form-button {
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-btn {
  position:relative;
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

.error {
  color: red;
  font-size: 0.9em;
  margin-top: 0.5em;
}
</style>
