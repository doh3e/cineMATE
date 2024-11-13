<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'Home' }">Home</RouterLink>
      <!-- 유저 정보가 없으면 로그인/회원가입 링크 표시 -->
      <RouterLink v-if="!store.userInfo || !store.userInfo.pk" :to="{ name: 'SignUp' }">Signup</RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.pk" :to="{ name: 'Login' }">Login</RouterLink>
      <!-- 유저 정보가 있으면 로그아웃 버튼 표시 -->
      <button v-else @click="handleLogout">Logout</button>
    </nav>
  </div>

  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useCounterStore } from './stores/counter'

const store = useCounterStore()
const router = useRouter()

onMounted(async () => {
  await store.getUserInfo()
  console.log('유저 정보:', store.userInfo); 
})

// 로그아웃 처리 함수
const handleLogout = async () => {
  try {
    await store.logout()
    alert('로그아웃 되었습니다!')
    router.replace('/')
  } catch (error) {
    console.error('로그아웃 오류:', error)
  }
}
</script>
