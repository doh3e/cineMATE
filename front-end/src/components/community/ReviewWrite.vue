<template>
  <div class="write-container">
    <h1 class="write-title">리뷰 작성</h1>
    <form @submit.prevent="submitReview" class="review-form">
      <div class="movieinfo userwrite-area">
        <div class="form-content title">
          <input type="text" id="title" v-model="formData.title" 
          placeholder="검색을 통해서만 영화 입력이 가능합니다" readonly />
          <button type="button" @click="openSearchModal">검색</button>
        </div>
        <div class="form-content review-title">
          <input
            type="text"
            id="review-title"
            v-model="formData.review_title"
            placeholder="한줄평을 입력하세요 (30자까지)"
            maxlength="30"
          />
        </div>
        <div class="form-content review-content">
          <textarea
            id="review-content"
            v-model="formData.review_content"
            placeholder="상세한 리뷰를 입력하세요"
          ></textarea>
        </div>
        <div class="form-content user-rating">
          <h3>나만의 별점</h3>
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
      <button type="submit" class="submit-btn">리뷰 작성</button>
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
  formData.value.id = movie.id
  formData.value.title = movie.title
  formData.value.overview = movie.overview
  formData.value.adult = movie.adult
  formData.value.popularity = movie.popularity
  formData.value.vote_average = movie.vote_average
  formData.value.genre_ids = movie.genre_ids
  formData.value.release_date = movie.release_date
  formData.value.poster_path = movie.poster_path
  closeSearchModal()
}

const selectedRating = ref(0)

const updateRating = (rating) => {
  selectedRating.value = rating
  formData.value.user_rating = rating
}

// 리뷰 제출
const submitReview = async () => {
  try {
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
  height: 100%;
}

.write-title {
  font-family: 'S-CoreDream';
  font-weight: 600;
  font-size: 2rem;
  margin-top: -20px;
  text-align: center;
  color: #f8f8f8;
}

.review-form {
  width: 100%;
  max-width: 600px;
  min-width: 400px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 15px;
  padding: 30px 0;
}

.movieinfo {
  width: 100%;
  padding: 20px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form-content {
  width: 80%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 2px solid #adadad;
  margin: 10px 30px;
  padding: 10px 10px;
}

.review-content {
  border-bottom: none;
}

#review-content {
  width: 400px;
  resize: none;
  border: none;
  border-radius: 5px;
  background-color: #f8f8f8;
  padding: 10px 20px;
  font-size: 0.9rem;
  word-wrap: break-word;
  line-height: 1.4;
  height: 150px;
  padding: 10px;
}

.title, .review-title {
  margin: 10px 30px;
  padding: 10px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

#title, #review-title {
  width: 100%;
  border:none;
  outline:none;
  color: #1f1f1f;
  font-size:16px;
  height:25px;
  background: none;
}

.title > button {
  width: 80px;
  height: 30px;
  border: none;
  border-radius: 10px;
  background-color: #f8f8f8;
  box-shadow: 1px 1px 1px #1f1f1f;
}

.info-typo {
  padding-top: 0;
  font-size: 0.9rem;
  color: red;
}

.user-rating {
  flex-direction: column;
  gap: 10px;
  border-bottom: none;
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

.auto-area {
  display: none;
}

.submit-btn {
  position:relative;
  margin-bottom: 20px;
  width:30%;
  height:40px;
  background: linear-gradient(125deg,#7469B6,#E1afd1,#AD88C6);
  background-position: left;
  background-size: 200%;
  color:white;
  font-weight: bold;
  border:none;
  cursor:pointer;
  transition: 0.4s;
  display:inline;
}

.submit-btn:hover {
  background-position: right;
  color: #1f1f1f;
}


</style>