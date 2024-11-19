<template>
  <div>
    <header class="header">
      <img src="@/assets/img/logo_imsi.png" alt="" class="header-logo">
      <Navbar :class="{ 'fixed-navbar': isNavbarFixed }" />
    </header>
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import Navbar from './components/Navbar.vue'
import { useAuthStore, useCounterStore } from './stores/counter';
import { useRoute } from 'vue-router';

const authStore = useAuthStore()
const store = useCounterStore()
const isNavbarFixed = ref(false)
const route = useRoute()

const handleScroll = () => {
  if (route.name === 'Home' || route.name === 'Movie' ) {
    isNavbarFixed.value = window.scrollY > 150
  } else {
    isNavbarFixed.value = false
  }
}


onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>

<style scoped>
.header {
  width: 100%;
  position: relative;
  z-index: 999; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.header-logo {
  width: 150px;
  object-fit: cover;
}

.fixed-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  opacity: 0.8;
  transition: opacity 0.3 ease;
}

.fixed-navbar:hover {
  opacity: 1;
}

</style>
