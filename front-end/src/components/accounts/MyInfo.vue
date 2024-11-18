<template>
  <div class="myinfo-box" v-if="person">
    <div class="profile-imgbox">
      <img v-if="person?.profile_image" :src="userImgPath" alt="profile-img" id="profile-img">
      <img v-else src="@/assets/img/default_profile_img.png" alt="profile-img" id="profile-img">
    </div>
    <div class="profile-content">
      <h3>{{ person?.nickname }} ({{ person?.username }})</h3>
      <p>이메일: {{ person?.email }}</p>
      <p>생일: {{ person?.birthday }}</p>
      <p>팔로워 수: {{ person?.followers.length }}</p>
      <p>팔로잉 수: {{ person?.followings.length }}</p>
    </div>
    <!-- 조건부로 정보 수정 버튼 렌더링 -->
    <button v-if="isEditAllowed" @click="$emit('editProfile')">정보 수정</button>
    <button
      v-if="isFollowVisible"
      @click="toggleFollow"
      :class="{ following: isFollowing }"
    >
      {{ isFollowing ? '언팔로우' : '팔로우' }}
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { authAxios } from '@/axios';

const props = defineProps({
  person: Object,
})

// 현재 로그인한 사용자 정보 가져오기
const store = useCounterStore()

// 사용자 프로필 이미지 경로
const userImgPath = computed(() => `http://127.0.0.1:8000${props.person?.profile_image}`)

// 정보 수정 버튼 표시 여부
const isEditAllowed = computed(() => props.person?.username === store.userInfo?.username)

// 팔로우 버튼 표시 여부 (자기 자신이 아닐 때만 표시)
const isFollowVisible = computed(() => props.person?.username !== store.userInfo?.username)

// 팔로우 상태
const isFollowing = computed(() => {
  return props.person?.followers?.includes(store.userInfo.username)
})

const emit = defineEmits(['updateRequired'])


const toggleFollow = async () => {
  try {
    const response = await authAxios.post(`/accounts/follows/${props.person.username}/`)
    console.log(response.data.is_followed)
    emit('updateRequired')
  } catch (error) {
    console.error('팔로우/언팔로우 오류:', error)
    alert('작업을 처리할 수 없습니다. 다시 시도해주세요.')
  }
}

</script>

<style scoped>
.myinfo-box {
  display: flex;
  gap: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}
#profile-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}
</style>
