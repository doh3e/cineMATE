<template>
  <div class="myinfo-box" v-if="person">
    <div class="profile-imgbox">
      <img v-if="userImgPath" :src="userImgPath" alt="profile-img" id="profile-img">
      <img v-else src="@/assets/img/default_profile_img.png" alt="profile-img" id="profile-img">
    </div>
    <div class="profile-content">
      <div class="default-info">
        <h2>{{ person?.nickname }} ({{ person?.username }})</h2>
        <span>{{ person?.email }}</span>
      </div>
      <div class="additional-info">
        <div class="follow-info">
          <span>{{ person?.birthday.slice(0,4)+'년 '
          +person?.birthday.slice(5,7)+'월 '
          +person?.birthday.slice(8,10)+'일 ｜ '
          || '일자 정보 없음'}}</span>
          <span>팔로워 <b>{{ person?.followers.length }}</b></span> ｜
          <span>팔로잉 <b>{{ person?.followings.length }}</b></span>
        </div>
        <div class="storage-info">
          <span>좋아한 영화 <b>{{ person?.liked_movies.length }}</b></span> ｜
          <span>보고싶은 영화 <b>{{ person?.bookmarked_movies.length }}</b></span>
        </div>
        <div class="review-info">
          <span>지금까지 <b>{{ person?.my_reviews.length }}</b> 건의 관측보고서를 작성했어요.</span>
        </div>
      </div>
      <div class="btn-area">
        <button v-if="isEditAllowed" @click="editProfile">정보 수정</button>
        <button
          v-if="isFollowVisible"
          @click="toggleFollow"
          :class="{ following: isFollowing }"
        >
          {{ isFollowing ? '언팔로우' : '팔로우' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { authAxios } from '@/axios';

const props = defineProps({
  person: Object,
})

const emit = defineEmits(['editProfile', 'updateRequired'])

const editProfile = () => {
  emit('editProfile')
}

const store = useCounterStore()

// 유저 프로필 이미지 있는지 확인 후 가져오는 함수
const userImgPath = computed(() => {
  const profileImage = props.person?.profile_image
  return profileImage ? `http://127.0.0.1:8000${profileImage}` : null
})


// 본인인지 (정보수정 가능한지) 확인
const isEditAllowed = computed(() => props.person?.username === store.userInfo?.username)

// 팔로우 버튼이 보이는지 (본인이 아닌지) 확인
const isFollowVisible = computed(() => props.person?.username !== store.userInfo?.username)

// 팔로우 중인지 확인
const isFollowing = computed(() => {
  return props.person?.followers?.includes(store.userInfo.username)
})

// 팔로우 버튼 기능
const toggleFollow = async () => {
  try {
    const response = await authAxios.post(`/accounts/follows/${props.person.username}/`)
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
  justify-content: space-evenly;
  align-items: center;
  width: 80%;
  max-width: 600px;
  min-width: 400px;
  height: 25vh;
  min-height: 250px;
  max-height: 400px;
  gap: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.profile-imgbox {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 180px;
  height: 180px;
}

#profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.btn-area{
  align-self: flex-end;
  display: flex;
  justify-content: flex-end;
  width: 100px;
}

.btn-area > button {
  font-family: 'S-CoreDream';
  font-weight: 400;
  background-color: #AD88C6;
  border: 0;
  border-radius: 10px;
  box-shadow: 2px 2px 2px #1f1f1f;
  width: 100px;
  height: 40px;
}

.btn-area > button:hover {
  background-color: #7469B6;
  cursor: pointer;
}

.default-info {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  font-family: 'S-CoreDream'; 
  gap: 10px;
}

.default-info > h2 {
  font-weight: 600;
}

.additional-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 10px;
  font-family: 'S-CoreDream'; 
}

@media screen and (max-width: 900px) {
  .profile-imgbox {
    display: none;
  }

  .profile-content{
    width: 90%;
  }
  .default-info,
  .additional-info {
    align-self: flex-start;
  }
}

</style>
