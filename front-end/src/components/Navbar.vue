<template>
  <nav class="navbar">
    <div class="yesteryear-regular navbar__logo">CINEMATE</div>
    <ul :class="['navbar__menu', { active: isMenuActive }]">
      <RouterLink :to="{ name: 'Home' }">
        <li :class="{ 'current-page': $route.path === '/' }">메인</li>
      </RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'SignUp' }">
        <li :class="{ 'current-page': $route.path === '/signup' }">회원가입</li>
      </RouterLink>
      <RouterLink v-if="!store.userInfo || !store.userInfo.id" :to="{ name: 'Login' }">
        <li :class="{ 'current-page': $route.path === '/login' }">로그인</li>
      </RouterLink>
      <li
        v-if="store.userInfo && store.userInfo.id"
        class="dropdown-container"
        @mouseenter="toggleDropdown(true)"
        @mouseleave="toggleDropdown(false)"
      >
        <RouterLink :to="{ name: 'Movie' }">
          <span :class="{ 'current-page': $route.name == 'Movie' }">영화탐색</span>
        </RouterLink>
        <ul v-if="isDropdownOpen" class="dropdown-menu">
          <RouterLink :to="{ name: 'Movie' }">
            <li :class="{ 'current-page': $route.name === 'Movie' }">장르별보기</li>
          </RouterLink>
          <RouterLink :to="{ name: 'Search' }">
            <li :class="{ 'current-page': $route.name === 'Search' }">영화검색</li>
          </RouterLink>
          <RouterLink :to="{ name: 'MovieCuration' }">
            <li :class="{ 'current-page': $route.name === 'MovieCuration' }">큐레이팅</li>
          </RouterLink>
        </ul>
      </li>
      <li
        v-if="store.userInfo && store.userInfo.id"
        class="dropdown-container"
        @mouseenter="toggleDropdown(true)"
        @mouseleave="toggleDropdown(false)"
      >
        <RouterLink :to="{ name: 'Review' }">
          <span :class="{ 'current-page': $route.path.includes('/review') }">리뷰</span>
        </RouterLink>
        <ul v-if="isDropdownOpen" class="dropdown-menu">
          <RouterLink :to="{ name: 'ReviewList' }">
            <li :class="{ 'current-page': $route.name === 'ReviewList' }">리뷰목록</li>
          </RouterLink>
          <RouterLink :to="{ name: 'ReviewWrite' }">
            <li :class="{ 'current-page': $route.name === 'ReviewWrite' }">리뷰작성</li>
          </RouterLink>
        </ul>
      </li>
      <RouterLink v-if="store.userInfo && store.userInfo.id" :to="{ name: 'Movieforyou' }">
        <li :class="{ 'current-page': $route.path === '/movieforyou' }">무비포유</li>
      </RouterLink>
      <RouterLink v-if="store.userInfo && store.userInfo.id" :to="{ name: 'Mypage', params: { username: store.userInfo.username } }">
        <li :class="{ 'current-page': $route.path === `/mypage/${store.userInfo.username}` }">나의소행성</li>
      </RouterLink>
      <li v-if="store.userInfo && store.userInfo.id" @click="handleLogout">로그아웃</li>
    </ul>
    <a href="#" class="navbar__toggleBtn" @click="toggleMenu">
      <i class="fa-solid fa-bars fa-xl" style="color: #F8F8F8;"></i>
    </a>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useCounterStore } from '../stores/counter'
import { useRouter, useRoute } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const isMenuActive = ref(false)
const isDropdownOpen = ref(false)
const navbarHeight = ref('auto')

// 메뉴 열릴 때 높이 계산
const calculateNavbarHeight = () => {
  const navbarMenu = document.querySelector('.navbar__menu')
  if (navbarMenu) {
    navbarHeight.value = isMenuActive.value
      ? `${navbarMenu.scrollHeight}px` // 열렸을 때 높이
      : '0px' // 닫혔을 때 높이
  }
}

// 드롭다운 열기/닫기 상태
const toggleDropdown = (state) => {
  isDropdownOpen.value = state
  nextTick(calculateNavbarHeight)
}

// 로그아웃 처리
const handleLogout = async () => {
  try {
    await store.logout()
  } catch (error) {
    console.error('로그아웃 오류:', error)
  }
}

// 메뉴 열고 닫기
const toggleMenu = () => {
  isMenuActive.value = !isMenuActive.value
  nextTick(() => {
    calculateNavbarHeight()
  })
}

// 화면 크기 변화에 따른 메뉴 초기화
onMounted(() => {
  const resetMenuOnResize = () => {
    if (window.innerWidth > 980) {
      isMenuActive.value = false // 데스크탑에서는 닫힘 상태 유지
    }
    calculateNavbarHeight()
  }
  window.addEventListener('resize', resetMenuOnResize)
  calculateNavbarHeight()
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateNavbarHeight)
})
</script>


<style scoped>

.navbar {
  position: sticky;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #7469B6;
  padding: 20px 12px;
  font-family: 'NotoSansKR';
  padding-left: 0;
  z-index: 9999;
  opacity: 0.9;
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
  font-family: 'S-CoreDream-3Light';
  font-size: 1.5rem;
  color: #F8F8F8;
  padding: 8px 30px;
  text-align: center;
  font-weight: 900;
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
  width: 100px;
}

.dropdown-menu li::after {
  content: none;
}

.dropdown-menu li:hover::after {
  content: none;
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

.dropdown-container {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #AD88C6;
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

@media screen and (max-width: 900px) {
  .navbar {
    flex-direction: column;
    transition: height 0.3s ease; /* 높이 전환 효과 추가 */
    overflow: hidden; /* 높이가 줄어들 때 잘리지 않도록 처리 */
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
    display: flex;
    justify-content: center;
    align-items: center;
    vertical-align: middle;
    width: 100%;
    color: #F8F8F8;
    text-align: center;
    font-size: 2.5rem;
  }

  .navbar__menu {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    max-height: 0px;
    opacity: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, opacity 0.3s ease;
  }

  .navbar__menu.active {
    max-height: 500px;
    opacity: 1;
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
    box-sizing: border-box;
    padding: 15px 8px;
    text-align: center;
    display: flex;
    justify-content: center;
    position: relative;
    cursor: pointer;
  }

  .navbar__menu li::after {
    content: none;
  }

  .dropdown-container {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }

  .dropdown-menu {
    position: absolute; /* 부모 메뉴의 위치 기준 */
    left: 57%;
    top:10%;
    background-color: #AD88C6;
    list-style: none;
    padding: 10px 0;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 200px; /* 드롭다운 메뉴의 너비 */
    max-height: 0;
    opacity: 0;
    visibility: hidden;
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    z-index: 99;
  }

  .dropdown-container:hover > .dropdown-menu,
  .dropdown-container.active > .dropdown-menu {
    max-height: 300px; /* 드롭다운이 열렸을 때의 최대 높이 */
    opacity: 1;
    visibility: visible;
  }

  .dropdown-menu a {
    width: 100%;
    margin: 0 auto;
  }

  .dropdown-menu li {
    width: 100%;
    padding: 10px 15px;
    text-align: center;
    color: #F8F8F8;
    transition: color 0.3s ease;
    white-space: nowrap; /* 텍스트 잘림 방지 */
  }

  .dropdown-menu li:hover {
    color: #1F1F1F;
  }
}

</style>
