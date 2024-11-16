<template>
  <nav class="navbar">
    <div class="navbar__logo">cineMATE</div>
    <ul :class="['navbar__menu', { active: isMenuActive }]">
      <RouterLink :to="{ name: 'Home' }">
        <li :class="{ 'current-page': $route.path === '/' }">HOME</li>
      </RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'SignUp' }">
        <li :class="{ 'current-page': $route.path === '/signup' }">회원가입</li>
      </RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'Login' }">
        <li :class="{ 'current-page': $route.path === '/login' }">로그인</li>
      </RouterLink>
      <!-- 드롭다운 메뉴 -->
      <li
        v-if="store.userInfo && store.userInfo.id"
        class="dropdown-container"
        @mouseenter="toggleDropdown(true)"
        @mouseleave="toggleDropdown(false)"
      >
        <RouterLink :to="{ name: 'Movie' }">
          <span :class="{ 'current-page': $route.path.includes('/movie') }">영화탐색</span>
        </RouterLink>
        <ul v-if="isDropdownOpen" class="dropdown-menu">
          <RouterLink :to="{ name: 'MovieSearch' }">
            <li :class="{ 'current-page': $route.name === 'MovieSearch' }">영화검색</li>
          </RouterLink>
          <RouterLink :to="{ name: 'MovieCurating' }">
            <li :class="{ 'current-page': $route.name === 'MovieCurating' }">큐레이팅</li>
          </RouterLink>
        </ul>
      </li>
      <RouterLink v-if="store.userInfo && store.userInfo.id" :to="{ name: 'Movieforyou' }">
        <li :class="{ 'current-page': $route.path === '/movieforyou' }">무비포유</li>
      </RouterLink>
      <RouterLink v-if="store.userInfo && store.userInfo.id" :to="{ name: 'Mypage' }">
        <li :class="{ 'current-page': $route.path === '/mypage' }">나의 소행성</li>
      </RouterLink>
      <li v-if="store.userInfo && store.userInfo.id" @click="handleLogout">로그아웃</li>
    </ul>
    <a href="#" class="navbar__toggleBtn" @click="toggleMenu">
      <i class="fa-solid fa-bars fa-xl" style="color: #F8F8F8;"></i>
    </a>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useCounterStore } from '../stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const navbarOpacity = ref(1)
const isMenuActive = ref(false)
const isDropdownOpen = ref(false)

const handleScroll = () => {
  navbarOpacity.value = window.scrollY > 150 ? 0.8 : 1
}

const handleMouseEnter = () => {
  navbarOpacity.value = 1
}

const handleMouseLeave = () => {
  navbarOpacity.value = window.scrollY > 150 ? 0.8 : 1
}

const toggleDropdown = (state) => {
  isDropdownOpen.value = state
}

const handleLogout = async () => {
  try {
    await store.logout()
    alert('로그아웃 되었습니다!')
    router.replace('/')
    window.location.reload()
  } catch (error) {
    console.error('로그아웃 오류:', error)
  }
}

const toggleMenu = () => {
  isMenuActive.value = !isMenuActive.value
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  position: relative;
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  font-family: 'TTLaundryGothicB';
  font-size: 1.5rem;
  color: #F8F8F8;
  padding: 8px 40px;
  text-align: center;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s ease;
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

.navbar__menu li:hover {
  color: #1F1F1F;
}

.navbar__menu li:hover::after {
  width: 50%;
}

.navbar__menu .current-page {
  color: #1F1F1F;
}

.navbar__menu .current-page::after {
  width: 50%;
}

.navbar__toggleBtn {
  position: absolute;
  right: 15px;
  display: none;
  z-index: 1;
}

/* 드롭다운 */ 
.dropdown-container {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #7469B6;
  list-style: none;
  padding: 15px 0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 250px; /* 드롭다운 크기 유지 */
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dropdown-container:hover > .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu li {
  padding: 12px 20px;
  font-size: 1.2rem;
  color: #F8F8F8;
  transition: color 0.3s ease;
}

.dropdown-menu li:hover {
  color: #1F1F1F;
}


/* 화면이 작을 경우 */

@media screen and (max-width: 900px) {

  .navbar {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20px 20px;
  }

  .navbar__toggleBtn {
    display: block;
    position: absolute;
    right: 30px;
    top: 30px;
    font-size: 1.5rem;
    color: #F8F8F8;
    cursor: pointer;
    transition: max-height 0.3s ease;
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
    width: 100%;
  }

  .navbar__menu {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    width: 100%;
    gap: 10px;
  }

  .navbar__menu > a {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .navbar__menu.active {
    max-height: 500px;
    opacity: 1;
  }

  .navbar__menu li {
    width: 100%;
    padding: 15px 8px;
    text-align: center;
    display: flex;
    justify-content: center;
    position: relative;
    cursor: pointer;
  }

  .navbar__menu li::after {
    content: none; /* 밑줄 제거 */
  }


  /* 드롭다운 메뉴 스타일 */
  .dropdown-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 15px;
  }

  .dropdown-menu {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 90%;
    max-height: 0;
    overflow: hidden;
    background-color: #7469B6;
    border-radius: 5px;
    transition: max-height 0.3s ease, opacity 0.3s ease, background-color 0.3s ease;
    opacity: 0;
  }

  li:hover > .dropdown-menu {
    max-height: 300px;
    opacity: 1;
    background-color: #AD88C6;
  }

  .dropdown-menu li {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    padding: 10px 15px;
    margin-left: 5px;
    text-align: left;
    color: #F8F8F8;
    transition: color 0.3s ease;
  }

  .dropdown-menu li:hover {
    color: #1F1F1F;
  }
}

</style>
