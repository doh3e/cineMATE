<template>
  <div class="review-container">
    <h1 class="yesteryear-regular h1-cali">🌘Review Board</h1>
    <div class="container-header">
      <button @click="goToList">리뷰목록</button>
      <button v-if="!isWriteMode" @click="goToWrite">리뷰작성</button>
    </div>
    <RouterView />
  </div>
</template>


<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ReviewList from '@/components/community/ReviewList.vue';
import ReviewWrite from '@/components/community/ReviewWrite.vue';
import ReviewDetail from '@/components/community/ReviewDetail.vue';

const route = useRoute()
const router = useRouter()


const isWriteMode = computed(() => route.name === 'ReviewWrite')

const goToList = () => {
  router.push({ name: 'ReviewList' })
}

const goToWrite = () => {
  router.push({ name: 'ReviewWrite' })
}

</script>


<style scoped>

.review-container {
  width: 80%;
  min-width: 1000px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
}

.container-header {
  width: 100%;
  min-width: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.container-header > button {
  position:relative;
  margin-bottom: 40px;
  width:20%;
  max-width: 300px;
  min-width: 150px;
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
  transition: background-position, color 0.3s ease;
}

.container-header > button:hover {
  background-position: right;
  color: #1f1f1f;
}

@media screen and (max-width: 900px) {
  .review-container {
    width: 100%;
    min-width: 0;
    padding: 0 15px;
  }

  .container-header {
    width: 100%;
    margin-top: 20px;
  }
}
</style>