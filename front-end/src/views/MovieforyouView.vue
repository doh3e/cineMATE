<template>
  <div class="mvforyou-container">
    <h1 class="yesteryear-regular h1-cali">🌘Movie for you</h1>
    <h1 class="subtitle">내 친구, 가족, 지인은 어떤 영화와 닮았을까?</h1>

    <div class="start-button">
      <button type="button" class="btn start-btn"
      @click="showTestPopup = true">테스트 시작하기!</button>
    </div>
    <div class="test-example"></div>
  </div>
  <div v-if="showTestPopup" class="popup-overlay">
    <div class="popup-content">
      <button class="close-button" @click="showTestPopup = false">✖</button>
      <MovieforYouTest v-if="showTestPopup"
      @close="showTestPopup = false" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieforYouTest from '@/components/community/MovieforYouTest.vue'

const showTestPopup = ref(false)

</script>

<style scoped>

.mvforyou-container {
  width: 80%;
  padding-top: 60px;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 20px;
}

.subtitle {
  text-align: center;
  font-family: 'S-CoreDream-3Light';
  font-size: 1.5rem;
  color: #f8f8f8;
}

.start-button {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.start-btn {
  position:relative;
  margin-bottom: 40px;
  width:20%;
  max-width: 400px;
  min-width: 200px;
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

.start-btn:hover {
  background-position: right;
}

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
  min-width: 600px;
  min-height: 800px;
  position: relative;
  background: white;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  text-align: center;
  height: 800px;
}

.close-button {
  position: absolute;
  z-index: 30000;
  top: 0px;
  right: 10px;
  background: none;
  border: none;
  font-size: 3rem;
  cursor: pointer;
  color: inherit;
}

.close-button:hover {
  color: red;
}
</style>