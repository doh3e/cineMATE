<template>
  <div class="app-container" @mousemove="handleMouseMove">
    <Navbar/>
    <main class="main-container">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router';

</script>

<style scoped>

.app-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  margin: 0 auto;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

.main-container {
  width: 90%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

input, select, textarea, option {
  cursor: inherit !important;
}

</style>
