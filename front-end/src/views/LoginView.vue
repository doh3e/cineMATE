<template>
  <div class="bg-video">
    <video class="bg-video__content" autoplay muted loop>
      <source src="@/assets/img/background_movie.mp4" type="video/mp4" />
      <source src="@/assets/img/background_movie.mp4" type="video/webm" />
    </video>
  </div>
  <div class="bg-black"></div>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2 class="h2-cali yesteryear-regular">Login</h2>
      <div class="text-form">
        <input v-model="form.username" type="text" id="username" placeholder="아이디" required />
      </div>
      <div class="text-form">
        <input v-model="form.password" type="password" id="password" placeholder="비밀번호" required />
      </div>
      <button type="submit" class="btn submit-btn">로그인</button>
    </form>
    <div class="find-anchor">
      <a href="">아이디 찾기</a>
      <a href="">비밀번호 찾기</a>
    </div>
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

* {
  margin: 0px;
  padding: 0px;
  text-decoration: none;
  overflow: hidden;
}

.bg-video {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 1;
  opacity: 1;
}

.bg-video__content {
  width: 100%;
  height: 100vh;
  object-fit: cover;
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
  z-index: -2;
  opacity: 1;
  background-color: #1f1f1f;
  overflow: hidden;
}

.login-container {
  position: relative;
  width: 400px;
  min-width: 400px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

.login-form {
  width: 400px;
  min-width: 400px;
  height: 400px;
  padding: 30px, 20px;
  background-color: rgba(255, 255, 255, 0.7);
  text-align:center;
  z-index: 3;
  transform: translateY(-50%);
  border-radius: 15px;
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

#username {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

#password {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

.find-anchor{
  margin-top: -250px;
  width: 350px;
  min-width: 350px;
  max-width: 350px;
  display: flex;
  z-index: 4;
  justify-content: space-between;
  align-items: center;
}

.find-anchor > a {
  text-align: center;
  color: #3f3f3f;
  transition: color 0.3 ease;
  cursor: pointer;
}

.find-anchor > a:hover {
  color: #7469B6;
}

.submit-btn {
  position:relative;
  margin-bottom: 40px;
  width:40%;
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
}
</style>
