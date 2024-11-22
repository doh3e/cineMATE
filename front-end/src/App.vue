<template>
  <div class="app-container" @mousemove="handleMouseMove">
    <Navbar/>
    <main class="main-container">
      <RouterView />
    </main>
    <div class="page-cursor" :style="cursorStyle">
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router';

const cursorStyle = ref({
  top: '0px',
  left: '0px',
})

let animationFrameId = null

const handleMouseMove = (event) => {
  if (animationFrameId) return
  animationFrameId = requestAnimationFrame(() => {
    const { clientX, clientY } = event
    cursorStyle.value = {
      top: `${clientY - 40}px`,
      left: `${clientX - 40}px`,
    }
    animationFrameId = null
  })
}

</script>

<style scoped>

.page-cursor {
  pointer-events: none;
  position: absolute;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  top: 0;
  left: 0;
  border: 2px solid #E1AFD1;
  transform: translate(15px, 15px);
  transition: transform 0.3s linear;
  opacity: 0.8;
  z-index: 20000;
  box-shadow: 2px 2px 2px black;
}

.app-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  width: 100%;
}

.main-container {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

</style>
