<template>
  <div class="mvforyou-container">
    <h1>무비포유</h1>
    <p>내 친구, 가족, 연인은 어떤 영화와 닮았을까?</p>
    <button @click="showTestPopup = true">테스트하러가기</button>
    <div v-if="showTestPopup" class="popup-overlay">
      <div class="popup-content">
        <button class="close-button" @click="showTestPopup = false">✖</button>
        <MovieforYouTest v-if="showTestPopup"
        @close="showTestPopup = false" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieforYouTest from '@/components/community/MovieforYouTest.vue'

const showTestPopup = ref(false)

</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  position: relative;
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
  text-align: center;
}
/* X 버튼 스타일 */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.close-button:hover {
  color: red;
}
</style>