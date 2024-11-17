<template>
  <div class="mypage-container">
    <div class="mypage-title">
      <h1>소행성 MV-{{store.userInfo.username}}</h1>
    </div>
    <div class="mypage-listtab">
      <button>내정보</button>
      <button>내가쓴글</button>
    </div>
    <div class="mypage-content" v-if="mypageData">
      <div class="mypage-mycard">
        <MyInfo
        :person="mypageData"
        />
        <MyAchievements/>
      </div>
      <div class="mypage-mymovie">
        <MyBookmarks
        :bookmarks="mypageData?.bookmarked_movies"
        />
        <MyLikes
        :likes="mypageData?.liked_movies"
        />
      </div>
    </div>
  </div>
</template>

<script setup>

import { useCounterStore } from '@/stores/counter';
import { publicAxios, authAxios } from '@/axios';
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue';
import MyBookmarks from '@/components/accounts/MyBookmarks.vue';
import MyLikes from '@/components/accounts/MyLikes.vue';
import MyInfo from '@/components/accounts/MyInfo.vue';
import MyAchievements from '@/components/accounts/MyAchievements.vue';

const store = useCounterStore()
const route = useRoute()
const username = route.params.username
const mypageData = ref(null)

const fetchMypage = async () => {
  try {
    const response = await publicAxios.get(`/accounts/mypage/${username}/`)
    mypageData.value = response.data
    console.log(mypageData.value)
  }
  catch(error){
    console.log('마이페이지 로드에 문제가 발생했습니다', error)
  }
}

onMounted(() => {
  fetchMypage()
})

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