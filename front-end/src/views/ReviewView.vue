<template>
  <div class="review-container">
    <div class="container-header">
      <button @click="goToList">리뷰 목록 보기</button>
      <button v-if="!isWriteMode" @click="goToWrite">리뷰 작성하기</button>
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
  margin-top: 50px;
  width: 100%;
  min-width: 1000px;
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