<template>
  <nav class="navbar" :style="{ opacity: navbarOpacity }" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
    <div class="navbar__logo">cineMATE</div>
    <ul class="navbar__menu">
      <RouterLink :to="{ name: 'Home' }">
        <li :class="{ 'current-page': $route.path === '/' }">HOME</li>
      </RouterLink>

      <!-- 로그인 상태에 따른 메뉴 표시 -->
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'SignUp' }">
        <li :class="{ 'current-page': $route.path === '/signup' }">회원가입</li>
      </RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'Login' }">
        <li :class="{ 'current-page': $route.path === '/login' }">로그인</li>
      </RouterLink>

      <!-- 로그인 상태일 경우 -->
      <RouterLink v-if="store.userInfo && store.userInfo.id" :to="{ name: 'Mypage' }">
        <li :class="{ 'current-page': $route.path === '/mypage' }">마이페이지</li>
      </RouterLink>
      <li v-if="store.userInfo && store.userInfo.id" @click="handleLogout">로그아웃</li>
    </ul>
    <a href="#" class="navbar__toggleBtn" @click="toggleMenu">
      <i class="fa-solid fa-bars fa-xl" style="color: #F8F8F8;"></i>
    </a>
  </nav>
</template>

<script setup>
import { useCounterStore } from '../stores/counter'
import { useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'

const store = useCounterStore()
const router = useRouter()

// 초기 navbar 불투명도 설정
const navbarOpacity = ref(1)

// 스크롤에 따른 navbar 불투명도 변경
const handleScroll = () => {
  navbarOpacity.value = window.scrollY > 150 ? 0.8 : 1
}

// 마우스 hover 시 opacity 변경
const handleMouseEnter = () => {
  navbarOpacity.value = 1
}

const handleMouseLeave = () => {
  navbarOpacity.value = window.scrollY > 150 ? 0.8 : 1
}

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

// 메뉴 토글 함수 (모바일에서)
const toggleMenu = () => {
  const menu = document.querySelector('.navbar__menu')
  menu.classList.toggle('active')
}

// 컴포넌트 마운트 시 스크롤 이벤트 리스너 추가
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

// 컴포넌트 언마운트 시 이벤트 리스너 제거
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #7469B6;
  padding: 20px 12px;
  font-family: 'NotoSansKR';
  padding-left: 0;
  transition: opacity 0.3s ease;
}

.navbar__logo {
  display: none;
  color: #F8F8F8;
  padding-left: 0;
}

.navbar__menu {
  list-style: none;
  display: flex;
  margin: 0;
  padding-left: 0;
}

.navbar__menu li {
  position: relative;
  font-family: 'TTLaundryGothicB';
  font-size: 1.5rem;
  color: #F8F8F8;
  padding: 8px 40px;
  text-align: center;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar__menu li::after {
  content: '';
  position: absolute;
  display: inline-block;
  width: 0;
  height: 2px;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #1F1F1F;
  transition: width 0.3s ease;
}

.navbar__menu li:hover::after {
  width: 50%;
}

.navbar__menu li:hover {
  color: #1F1F1F;
}

.navbar__menu .current-page::after {
  width: 50%;
}

.navbar__menu .current-page {
  color: #1F1F1F;
}

.navbar__toggleBtn {
  position: absolute;
  right: 15px;
  display: none;
  z-index: 1;
}

@media screen and (max-width: 700px) {
  .navbar__toggleBtn {
    display: block;
    position: absolute;
    right: 30px;
    top: 30px;
  }

  .navbar__logo {
    display: block;
    font-family: 'TTLaundryGothicB';
    width: 100%;
    color: #F8F8F8;
    text-align: center;
    font-size: 2.5rem;
  }

  .navbar {
    flex-direction: column;
    align-items: flex-start;
    margin: 0;
  }

  .navbar__menu {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    flex-direction: column;
    align-items: center;
    width: 100%;
    gap: 10px;
  }

  .navbar__menu.active {
    margin-top: 20px;
    max-height: 500px;
    opacity: 1;
  }

  .navbar__menu li {
    width: 100%;
    padding: 15px 8px;
    text-align: center;
    display: flex;
    justify-content: center;
  }

  .navbar__menu li:hover {
    color: #1F1F1F;
  }

  .navbar__menu li:hover::after {
    width: 20%;
  }

  .navbar__menu .current-page::after {
    width: 20%;
  }

  .navbar__icons {
    display: none;
    justify-content: center;
  }
}
</style>
