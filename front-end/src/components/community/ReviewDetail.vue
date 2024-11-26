<template>
  <div class="rvdetail-container" v-if="review">
    <div class="rv-title-box">
    <h1 class="rv-review-title">{{ review?.review_title }}</h1>
    <h3 class="rv-title">영화 < {{ review?.title }} > 리뷰</h3>
    </div>
    <div class="rv-box writer">
      <p @click="goMypage(review.user.username)"><strong>작성자 ｜</strong>
        {{ review?.user?.nickname }}({{ review?.user?.username }})</p>
      <p>{{ formatDate(review?.created_at) }}</p>
    </div>
    <hr>
    <div class="rv-box review-content">
      <span id="user-star-desc">{{ review?.user.nickname }} 메이트님은 아래와 같은 평가를 내렸어요.</span>
      <div class="user-star">
        <span v-for="num in parseInt(review.user_rating)" :key="num">
          <img src="@/assets/img/full-star.png" alt="Half Star" class="star" />
        </span>
        <span v-for="num in (5 - parseInt(review.user_rating))" :key="num">
          <img src="@/assets/img/empty-star.png" alt="Empty Star" class="star" />
        </span>
      </div>
      <div class="review-content-box"> 
        <p>{{ review?.review_content }}</p>
      </div>
    </div>
    <div class="rv-box movieinfo">
      <div class="movie-poster" @click="openMovieModal(review)">
        <img :src="store.getImageUrl(review?.poster_path)" alt="poster image" class="poster-image" v-if="review.poster_path">
        <img src="@/assets/img/default_movie_poster.png" alt="default poster image" class="poster-image" v-else>
      </div>
      <div class="movie-desc">
        <h3 id="desc-title" @click="openMovieModal(review)">{{ review?.title }} ({{ review?.release_date.slice(0,4) }})</h3>
        <div class="genre-box">
          <div v-for="genre in review?.genre_names" :key="genre" class="genre-id">
            {{ genre }}
          </div>
        </div>
        <div class="desc-overview">
          <p>{{ review?.overview }}</p>
        </div>
      </div>
      <div class="desc-vote">
        <span id="vote-num">평점 ｜ {{ review?.vote_average }}</span>
        <span v-for="n in reviewStars.fullStars" :key="'review-full-' + n">
          <img src="@/assets/img/full-star.png" alt="Full Star" class="star" />
        </span>
        <span v-if="reviewStars.hasHalfStar">
          <img src="@/assets/img/half-star.png" alt="Half Star" class="star" />
        </span>
        <span v-for="n in reviewStars.emptyStars" :key="'review-empty-' + n">
          <img src="@/assets/img/empty-star.png" alt="Empty Star" class="star" />
        </span>
      </div>
    </div>
    <div class="interaction">
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
      <div class="btns">
        <button v-if="isUserOwner" @click="goToEdit">수정</button>
        <button v-if="isUserOwner" @click="goToDelete">삭제</button>
        <button @click="goBackToList">목록</button>
      </div>
    </div>
    <ReviewEditModal
      v-if="isEditModalOpen"
      :isOpen="isEditModalOpen"
      :review="review"
      :onClose="closeEditModal"
      :onUpdate="updateReview"
    />
  </div>
  <ReviewComment
    v-if="review"
    :review_id="review?.review_id"
  />
  <MovieDetail
  v-if="isMovieModalVisible"
  :movie="selectedMovie"
  :isVisible="isMovieModalVisible"
  @close="closeMovieModal"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAxios, publicAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter';
import ReviewEditModal from './ReviewEditModal.vue';
import ReviewComment from './ReviewComment.vue';
import MovieDetail from '../movies/MovieDetail.vue';

const route = useRoute()
const router = useRouter()
const review = ref(null)
const store = useCounterStore()
const isEditModalOpen = ref(false)
const isLikeAnimating = ref(false)

const isLiked = computed(() => {
  return review.value?.liked_users?.includes(store.userInfo?.id)
})

// 작성자를 누르면 마이페이지로 이동
const goMypage = (username) => {
  router.push({name: 'Mypage', params: {username: username}})
}

// 디테일 모달창
const selectedMovie = ref(null)
const isMovieModalVisible = ref(false)

const openMovieModal = (movie) => {
  selectedMovie.value = movie
  isMovieModalVisible.value = true
}

const closeMovieModal = () => {
  isMovieModalVisible.value = false
}

// 리뷰 좋아요 로직
const toggleLike = async () => {
  if(store.userInfo.username === review.value.user.username){
    alert('자기 자신의 리뷰에는 좋아요를 누를 수 없습니다!')
    return
  }
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
    hour12: false,
  })
}

// 영화 평점 별로 치환
const reviewStars = computed(() => {
  return calculateStars(review.value?.vote_average || 0)
})

const calculateStars = (rating) => {
  const maxStars = 5
  const roundedRating = Math.round(rating) / 2
  const fullStars = Math.floor(roundedRating)
  const hasHalfStar = roundedRating % 1 !== 0
  const emptyStars = maxStars - fullStars - (hasHalfStar ? 1 : 0)

  return { fullStars, hasHalfStar, emptyStars }
}

// 로그인한 유저가 리뷰 주인인지 판단
const isUserOwner = computed(() => {
  return store.userInfo?.id === review.value?.user?.id
})

// 수정하기
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
  review.value = updatedReview
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
  width: 90%;
  min-width: 450px;
  max-width: 800px;
  height: auto;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
}

.rv-title-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.rv-review-title {
  font-family: 'S-CoreDream';
  font-size: 2rem;
  width: 100%;
  text-align: center;
}

.rv-title {
  font-family: 'S-CoreDream';
  width: 100%;
  font-size: 1.1rem;
  text-align: center;
  margin-top: -15px;
}

hr {
  width: 100%;
}

.rv-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.writer {
  font-family: 'S-CoreDream';
  flex-direction: row;
  justify-content: space-between;
  cursor: pointer;
}

.user-star {
  width: 30%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-star img {
  width: 30px;
  height: 30px;
  margin-right: 2px;
}

#user-star-desc {
  font-family: 'S-CoreDream';
  font-weight: 600;
  margin-bottom: 10px;
}

.review-content-box {
  width: 90%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin: 20px;
}

.review-content-box > p {
  text-align: justify;
  line-height: 1.5;
}

.movieinfo {
  position: relative;
  width: 90%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: #DDD;
  border-radius: 10px;
  padding: 20px;
  gap:20px;
}

#desc-title {
  font-family: 'S-CoreDream';
  text-align: left;
}

.movie-poster {
  width: 15%;
  min-width: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.poster-image {
  width: 100%;
}

.movie-desc {
  width: 85%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap:15px;
}

.genre-box {
  font-family: 'S-CoreDream';
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}

.genre-box > div {
  width: auto;
  min-width: 60px;
  height: 25px;
  font-size: 0.9rem;
  border: none;
  border-radius: 30px;
  padding: 5px;
  background-color: #AAA;
  box-shadow: 1px 1px 1px #1f1f1f;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.desc-overview {
  background-color: rgba(248, 248, 248, 0.7);
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  height: 70px;
  padding: 15px 20px;
  overflow-y: scroll;
  box-sizing: border-box;
}

.desc-overview > p {
  width: 100%;
  height: auto;
  display: block;
  justify-content: center;
  align-items: flex-start;
  text-align: justify;
  line-height: 1.4;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.desc-vote {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  right: 20px;
  top: 20px;
}

.desc-vote > span > img {
  width: 25px;
}

#vote-num {
  font-family: 'S-CoreDream';
  font-weight: 600;
  font-size: 1.2rem;
  margin-right: 5px;
}

@media (max-width: 900px) {
  #vote-num {
    display: none;
  }
}

@media (max-width: 700px) {
  #vote-num {
    display: none;
  }
  .desc-vote{
    display: none;
  }
}


.interaction {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.likes {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.btns {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.btns > button {
  width: 50px;
  height: 30px;
  cursor: pointer;
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
