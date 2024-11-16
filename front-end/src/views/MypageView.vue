<template>
  <div class="mypage-container">
    <div class="mypage-title">
      <h1>소행성 MV-{{store.userInfo.username}}</h1>
    </div>
    <div class="mypage-listtab">
      <button>내정보</button>
      <button>내가쓴글</button>
    </div>
    <div class="mypage-content">
      <div class="mypage-mycard">
        <MyInfo/>
        <MyAchievements/>
      </div>
      <div class="mypage-mymovie">
        <MyBookmarks/>
        <MyLikes/>
      </div>
    </div>
  </div>
</template>

<script setup>

import { useCounterStore } from '@/stores/counter';
import MyBookmarks from '@/components/accounts/MyBookmarks.vue';
import MyLikes from '@/components/accounts/MyLikes.vue';
import MyInfo from '@/components/accounts/MyInfo.vue';
import MyAchievements from '@/components/accounts/MyAchievements.vue';

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