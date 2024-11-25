<template>
  <div class="rvdetail-container">
    <h1 class="rv-review-title">{{ review?.review_title }}</h1>
    <div class="rv-box writer">
      <p><strong>작성자:</strong> {{ review?.user?.nickname}}({{review?.user?.username }})</p>
      <p><strong>작성일:</strong> {{ formatDate(review?.created_at) }}</p>
    </div>
    <div class="rv-box movieinfo">
      <p><strong>영화 제목:</strong> {{ review?.title }}</p>
      <p><strong>장르:</strong></p>
      <ul>
        <li v-for="genre in review?.genre_names" :key="genre" class="genre-id">
          {{ genre }}
        </li>
      </ul>
      <p><strong>줄거리 : {{ review?.overview }} </strong></p>
      <p><strong>영화평점 : {{ review?.vote_average }} </strong></p>
    </div>
    <div class="rv-box review-content">
      <p><strong>유저평점:</strong> {{ review?.user_rating }}</p>
      <p><strong>리뷰내용:</strong> {{ review?.review_content }}</p>
      <button v-if="isUserOwner" @click="goToEdit">수정</button>
      <button v-if="isUserOwner" @click="goToDelete">삭제</button>
      <button @click="goBackToList">리뷰 목록으로</button>
      <ReviewEditModal
        v-if="isEditModalOpen"
        :isOpen="isEditModalOpen"
        :review="review"
        :onClose="closeEditModal"
        :onUpdate="updateReview"
      />
      <div class="likes" @click.stop="toggleLike">
        <span>
          <i
            :class="{
              'fa-regular': !isLiked,
              'fa-solid': isLiked,
              'animate': isLikeAnimating
            }"
            class="fa-heart fa-lg"
            :style="{ color: isLiked ? 'red' : '#B197FC' }"
            @animationend="isLikeAnimating = false"
          ></i>
        </span>
        <span v-if="review && review.like_count !== undefined">{{ review.like_count }}</span>
      </div>
    </div>
    <ReviewComment
      v-if="review"
      :review_id="review?.review_id"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAxios, publicAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter';
import ReviewEditModal from './ReviewEditModal.vue';
import ReviewComment from './ReviewComment.vue';

const route = useRoute()
const router = useRouter()
const review = ref(null)
const store = useCounterStore()
const isEditModalOpen = ref(false)
const isLikeAnimating = ref(false)

const isLiked = computed(() => {
  return review.value?.liked_users?.includes(store.userInfo?.id)
})

const toggleLike = async () => {
  try {
    const response = await authAxios.post(`/community/reviews/${route.params.review_id}/likes/`)
    review.value.like_count = response.data.like_count
    review.value.liked_users = response.data.liked_users
    isLikeAnimating.value = true
  } catch (error) {
    console.error('좋아요 토글 중 오류 발생:', error)
  }
}

const fetchReviewDetail = async () => {
  try {
    const response = await publicAxios.get(`/community/reviews/${route.params.review_id}/`)
    review.value = response.data
    console.log(response.data)
  } catch (error) {
    console.error('리뷰 데이터를 가져오는 중 오류 발생:', error)
  }
}

const goBackToList = () => {
  router.push({ name: 'ReviewList' })
}

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false, // 24시간 형식 사용
  })
}

const isUserOwner = computed(() => {
  return store.userInfo?.id === review.value?.user?.id
})

// 리뷰 수정 페이지로 이동
const goToEdit = () => {
  isEditModalOpen.value = true
}

// 리뷰 삭제
const goToDelete = async () => {
  if (!isUserOwner.value) {
    alert('이 리뷰를 삭제할 권한이 없습니다.')
    return
  }

  const isConfirmed = confirm('정말 이 리뷰를 삭제하시겠어요?')
  if (!isConfirmed) {
    return
  }

  try {
    await authAxios.delete(`/community/reviews/${route.params.review_id}/`)
    alert('리뷰를 삭제했습니다!')
    router.replace({ name: 'ReviewList' })
  } catch (error) {
    alert('리뷰를 삭제하는 중 오류가 발생했습니다!')
    console.error('리뷰를 삭제하는 중 오류 발생:', error)
  }
}


const closeEditModal = () => {
  isEditModalOpen.value = false
}

const updateReview = (updatedReview) => {
  review.value = updatedReview // 업데이트된 리뷰로 변경
}

onMounted(() => {
  fetchReviewDetail()
})

</script>

<style scoped>
.rvdetail-container {
  padding: 20px 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  max-width: 800px;
  height: 70%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 20px;
}

.rv-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.likes {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 5px;
}

.fa-heart {
  cursor: pointer;
  padding: 5px;
  transition: transform 0.3s ease, color 0.3s ease;
}

.fa-heart.animate {
  animation: pop 0.3s ease;
}

@keyframes pop {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}
</style>
