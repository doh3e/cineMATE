<template>
  <div class="modal-backdrop" v-if="isOpen">
    <div class="modal-content">
      <h3>리뷰 수정</h3>
      <form @submit.prevent="submitEdit">
        <p>영화 정보는 수정할 수 없습니다.</p>
        <div>
          <label>리뷰 제목</label>
          <input type="text" v-model="formData.review_title" />
        </div>
        <div>
          <label>리뷰 내용</label>
          <textarea v-model="formData.review_content" id="review-content"></textarea>
        </div>
        <div>
          <label for="user-rating">유저 평점</label>
          <div class="star-rating">
            <input
              v-for="n in 5"
              :key="n"
              type="radio"
              :id="'edit-star-' + n"
              name="user-rating"
              :value="n"
              v-model="selectedRating"
              @change="updateRating(n)"
            />
            <label
              v-for="n in 5"
              :key="'label-' + n"
              :for="'edit-star-' + n"
              class="star"
              :class="{ filled: n <= selectedRating }"
            >
              ★
            </label>
          </div>
        </div>
        <div class="button-group">
          <button type="submit">수정 완료</button>
          <button type="button" @click="closeModal">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { authAxios } from '@/axios'

// Props 정의
const props = defineProps(['isOpen', 'review', 'onClose', 'onUpdate'])

// 초기 변수 설정
const formData = ref({
  review_title: '',
  review_content: '',
  user_rating: 0,
})
const selectedRating = ref(0)

// 리뷰 데이터 동기화
watch(
  () => props.review,
  (newReview) => {
    if (newReview) {
      formData.value = { ...newReview }
      selectedRating.value = newReview.user_rating
    }
  },
  { immediate: true }
)

// 별점 업데이트
const updateRating = (rating) => {
  selectedRating.value = rating
  formData.value.user_rating = rating
}

// 수정 요청
const submitEdit = async () => {
  try {
    const response = await authAxios.put(
      `/community/reviews/${formData.value.review_id}/`,
      {
        review_title: formData.value.review_title,
        review_content: formData.value.review_content,
        user_rating: formData.value.user_rating
      }
    )
    alert('리뷰 수정이 완료되었습니다!')
    props.onUpdate(response.data)
    closeModal()
  } catch (error) {
    console.error('리뷰 수정 실패:', error)
    alert('수정 중 오류가 발생했습니다.')
  }
}

// 모달 닫기
const closeModal = () => {
  props.onClose()
}

</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.star-rating input[type='radio'] {
  display: none;
}

.star-rating .star {
  font-size: 2rem;
  cursor: pointer;
  color: #ccc;
  transition: color 0.2s ease-in-out;
}

.star-rating .star.filled {
  color: #ffc107;
}

.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

#review-content {
  width: 300px;
  height: 200px;
}

button {
  padding: 10px 20px;
  background-color: #7469b6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #5a4b99;
}

button[type='button'] {
  background-color: #ccc;
}

button[type='button']:hover {
  background-color: #aaa;
}
</style>
