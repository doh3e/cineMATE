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

const authStore = useAuthStore()
const store = useCounterStore()
const isNavbarFixed = ref(false)

const handleScroll = () => {
  isNavbarFixed.value = window.scrollY > 300
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
}

</style>
