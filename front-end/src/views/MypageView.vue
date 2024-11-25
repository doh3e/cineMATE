<template>
  <div class="mypage-container">
    <div class="mypage-title">
      <h1 class="yesteryear-regular h1-cali">🌌Planet of {{ route.params.username }}</h1>
      <h2 class="subtitle">{{ store.userInfo?.nickname }}의 소행성</h2>
    </div>
    <div class="mypage-listtab">
      <button @click="currentTab = 'info'" :class="{ active: currentTab === 'info' }">유저정보</button>
      <button @click="currentTab = 'storage'" :class="{ active: currentTab === 'storage' }">보관함</button>
      <button @click="currentTab = 'reviews'" :class="{ active: currentTab === 'reviews' }">나의리뷰</button>
    </div>
    <div class="mypage-content">
    <component
      v-if="mypageData"
      :is="currentComponent"
      :person="currentTab === 'info' ? mypageData : null"
      :bookmarks="currentTab === 'storage' ? mypageData?.bookmarked_movies : null"
      :likes="currentTab === 'storage' ? mypageData?.liked_movies : null"
      :myReviews="currentTab === 'reviews' ? mypageData?.my_reviews : []"
      :likedReviews="currentTab === 'reviews' ? mypageData?.liked_reviews : []"
      @editProfile="switchToEdit"
      @updateRequired="fetchMypage"
    />
      <UserEdit
        v-if="currentTab === 'edit'"
        @cancelEdit="currentTab = 'info'"
        @updateComplete="fetchMypage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { publicAxios } from '@/axios'
import { useRoute } from 'vue-router'
import MyInfo from '@/components/accounts/MyInfo.vue'
import MyStorage from '@/components/accounts/MyStorage.vue'
import MyReviews from '@/components/accounts/MyReviews.vue'
import UserEdit from '@/components/accounts/UserEdit.vue'

const store = useCounterStore()
const route = useRoute()

const currentTab = ref('info') // 현재 탭 상태
const mypageData = ref(null) // 마이페이지 데이터

// 탭 컴포넌트 매핑
const tabComponents = {
  info: MyInfo,
  storage: MyStorage,
  reviews: MyReviews,
}

// 현재 컴포넌트
const currentComponent = computed(() => tabComponents[currentTab.value])

// 마이페이지 데이터 불러오기
const fetchMypage = async () => {
  try {
    const username = route.params.username
    const response = await publicAxios.get(`/accounts/mypage/${username}/`)
    mypageData.value = response.data
    console.log(mypageData.value)
  } catch (error) {
    console.error('마이페이지 데이터 로드 오류:', error)
  }
}

// 정보 수정 화면으로 전환
const switchToEdit = () => {
  currentTab.value = 'edit'
}

onMounted(() => {
  fetchMypage()
})
</script>

<style scoped>
.mypage-container {
  width: 80%;
  min-width: 400px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 30px;
}

.mypage-title {
  width: 50%;
  margin: 0 auto;
  font-family: 'S-CoreDream';
  font-weight: 600;
  color: #f8f8f8;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.h1-cali {
  text-align: center;
}

.subtitle {
  text-align: right;
}

.mypage-listtab {
  display: flex;
  gap: 10px;
}

.mypage-listtab button {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-family: 'S-CoreDream-3Light';
  font-weight: 600;
}

.mypage-listtab button:hover {
  background-color: #AD88C6;
}

.mypage-listtab button.active {
  background-color: #7469B6;
  color: white;
}

.mypage-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  height: 100%;
}

.mypage-content > div {
  width: 100%;
}

</style>
