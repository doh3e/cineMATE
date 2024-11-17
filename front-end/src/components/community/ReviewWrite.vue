<template>
  <div class="write-container">
    <form @submit.prevent="submitReview" class="review-form">
      <div class="movieinfo userwrite-area">
        <div class="form-content title">
          <label for="title">영화 제목</label>
          <input type="text" id="title" v-model="formData.title" readonly />
          <button type="button" @click="openSearchModal">검색</button>
        </div>
        <p>검색을 통해서만 영화를 입력할 수 있습니다.</p>
        <div class="form-content review-title">
          <label for="review-title">리뷰 제목</label>
          <input
            type="text"
            id="review-title"
            v-model="formData.review_title"
            placeholder="리뷰 제목을 입력하세요"
          />
        </div>
        <div class="form-content review-content">
          <label for="review-content">리뷰내용</label>
          <textarea
            id="review-content"
            v-model="formData.review_content"
            placeholder="리뷰 내용을 입력하세요"
          ></textarea>
        </div>
        <div class="form-content user-rating">
          <label for="user-rating">별점</label>
          <div class="star-rating">
            <input
              v-for="n in 5"
              :key="n"
              type="radio"
              :id="'star-' + n"
              name="user-rating"
              :value="n"
              v-model="selectedRating"
              @change="updateRating(n)"
            />
            <label
              v-for="n in 5"
              :key="n"
              :for="'star-' + n"
              class="star"
              :class="{ filled: n <= selectedRating }"
            >
              ★
            </label>
          </div>
        </div>
      </div>
      <div class="movieinfo auto-area">
        <div class="form-content id">
          <label>영화코드</label>
          <input type="text" v-model="formData.id" readonly />
        </div>
        <div class="form-content overview">
          <label>개요</label>
          <textarea id="overview" v-model="formData.overview" readonly></textarea>
        </div>
        <div class="form-content adult">
          <label>성인여부</label>
          <input type="text" v-model="formData.adult" readonly />
        </div>
        <div class="form-content popularity">
          <label>유명도</label>
          <input type="text" v-model="formData.popularity" readonly />
        </div>
        <div class="form-content vote-average">
          <label>평점</label>
          <input type="text" v-model="formData.vote_average" readonly />
        </div>
        <div class="form-content genre-ids">
          <label>장르</label>
          <div class="genre-tags">
            <span
              v-for="id in formData.genre_ids"
              :key="id"
              class="genre-tag"
            >
              {{ id }}
            </span>
          </div>
        </div>
        <div class="form-content release-date">
          <label>개봉일</label>
          <input type="text" v-model="formData.release_date" readonly />
        </div>
        <div class="form-content poster-path">
          <label>포스터</label>
          <input type="text" v-model="formData.poster_path" readonly />
        </div>
      </div>
      <button type="submit">리뷰 작성</button>
    </form>

    <!-- 영화 검색 모달 -->
    <ReviewMovieSearchModal
      v-if="isModalOpen"
      @close="closeSearchModal"
      @select="selectMovie"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authAxios } from '@/axios';
import { useRouter } from 'vue-router';
import ReviewMovieSearchModal from './ReviewMovieSearchModal.vue';

const router = useRouter()

const isModalOpen = ref(false)
const formData = ref({
  review_title: '',
  review_content: '',
  user_rating: 0,
  id: '',
  title: '',
  overview: '',
  adult: false,
  popularity: 0,
  vote_average: 0,
  genre_ids: [],
  release_date: '',
  poster_path: ''
})

const openSearchModal = () => {
  isModalOpen.value = true
}

const closeSearchModal = () => {
  isModalOpen.value = false
}

// 영화 선택
const selectMovie = (movie) => {
  console.log('선택된 영화:', movie) // 디버깅 로그 추가
  formData.value.id = movie.id
  formData.value.title = movie.title
  formData.value.overview = movie.overview
  formData.value.adult = movie.adult
  formData.value.popularity = movie.popularity
  formData.value.vote_average = movie.vote_average
  formData.value.genre_ids = movie.genre_ids
  formData.value.release_date = movie.release_date
  formData.value.poster_path = movie.poster_path
  closeSearchModal() // 모달 닫기
}

const selectedRating = ref(0) // 사용자가 선택한 별점

const updateRating = (rating) => {
  selectedRating.value = rating
  formData.value.user_rating = rating
  console.log(`별점 ${rating} 선택됨`) // 선택된 별점 디버깅용 로그
}

// 리뷰 제출
const submitReview = async () => {
  try {
    console.log('폼 데이터:', formData.value)
    await authAxios.post('/community/reviews/', formData.value)
    alert('리뷰 작성이 완료되었습니다!')
    router.replace({ name: 'ReviewList' })
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
    alert('리뷰 작성 중 오류가 발생했습니다.')
  }
}
</script>


<style scoped>

.write-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin-bottom: 30px;
}
.review-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.movieinfo {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap:20px;
}

.form-content {
  width: 80%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

input[type=text] {
  width: 200px;
  height: 25px;
  border-radius: 5px; 
}

textarea {
  width: 400px;
  resize: none;
}

#title, #review-title {
  width: 350px;
}

#overview {
  height: 50px;
}

#review-content {
  height: 200px;
  padding: 10px;
}

.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.genre-tag {
  background-color: #f0f0f0;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.9rem;
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

</style>