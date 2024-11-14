<template>
  <div class="mypage-container">
    <div class="mypage-title">
      <h1>소행성 MV-{{store.userInfo.username}}</h1>
    </div>
    <div class="mypage-content">
      <div class="mypage-mycard">

      </div>
      <div class="mypage-mymovie">

      </div>
      <div class="mypage-myreview">
        
      </div>
    </div>
  </div>
</template>

<script setup>

import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()


</script>

<style scoped>
.mypage-container {
  width: 80%;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
}

</style>