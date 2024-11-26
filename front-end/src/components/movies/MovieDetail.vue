<template>
  <div v-if="movie && isVisible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-top">
        <div id="player-container" v-if="youtube_path"
        @mouseenter="onPlayerMouseEnter"
        @mouseleave="onPlayerMouseLeave"></div>
        <div v-else>
        <h1 class="yesteryear-regular h1-cali">No Trailers</h1>
        <img src="@/assets/img/projector-12629.gif" alt="default gif">
        </div>
      </div>
      <div class="modal-bottom">
        <div class="modal-bleft">
          <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" class="movie-poster">
          <img v-else src="@/assets/img/default_movie_poster.png" alt="Default Poster" class="movie-poster">
        </div>
        <div class="modal-bright">
          <h1 class="truncate detail-title">{{ movie.title }}</h1>
          <div class="movie-desc">
            <span>장르 ｜ {{ genreNames.join(', ') }}</span>
            <span>개봉 ｜ {{ movie.release_date.slice(0,4) }}</span>
            <div class="movie-rating">
              <span>평점 ｜ </span>
              <span v-for="n in fullStars" :key="'full-' + n">
                <img src="@/assets/img/full-star.png" alt="Full Star" class="star" />
              </span>
              <span v-if="hasHalfStar">
                <img src="@/assets/img/half-star.png" alt="Half Star" class="star" />
              </span>
              <span v-for="n in emptyStars" :key="'empty-' + n">
                <img src="@/assets/img/empty-star.png" alt="Empty Star" class="star" />
              </span>
            </div>
          </div>
          <div class="movie-overview">
            <p>{{ movie.overview }}</p>
          </div>
          <div class="user-reaction">
            <div class="user-review">
              <h3>유저리뷰</h3>
              <div class="review-box">
                <div class="review-item" v-if="reviewList.length > 0"
                v-for="review in reviewList"
                :key="review.review_id">
                <p>
                  <span v-for="num in review.user_rating">
                    <img src="@/assets/img/full-star.png" alt="Half Star" class="star" />
                  </span>
                  <span v-for="num in (5 - review.user_rating)">
                    <img src="@/assets/img/empty-star.png" alt="Empty Star" class="star" />
                  </span>
                </p>
                <p><span>❝ {{ review.review_title }} ❞</span> - {{ review.user.nickname }} 메이트</p>
                </div>
                <h3 v-else>아직 유저 리뷰가 없습니다.</h3>
              </div>
            </div>
            <div class="movie-stats ">
              <h3>메이트들의 선택</h3>
              <div v-if="movieStats" class="stat-box">
                <div class="stat">
                  <img src="@/assets/img/gradation-heart.png" alt="" class="stat-icon">
                  <h3>{{ movieStats.like_count }}</h3>
                </div>
                <div class="stat">
                  <img src="@/assets/img/gradation-bookmark.png" alt="" class="stat-icon">
                  <h3>{{ movieStats.bookmark_count }}</h3>
                </div>
                <div class="stat">
                  <img src="@/assets/img/gradation-flag.png" alt="" class="stat-icon">
                  <h3 v-if="movieStats.popularity_rank !== 'No Rank'">
                    {{ movieStats.popularity_rank }}
                  </h3>
                  <h3 v-else>
                    -
                  </h3>
                </div>
              </div>
              <p v-else>통계 데이터를 불러오는 중...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { computed, watch, ref, onMounted, onBeforeUnmount } from 'vue';
import { publicAxios } from '@/axios';

const store = useCounterStore();

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

// 평점 별로 치환하는 로직
const maxStars = 5
const roundedRating = computed(() => Math.round(props.movie?.vote_average) / 2)
const fullStars = computed(() => Math.floor(roundedRating.value))
const hasHalfStar = computed(() => roundedRating.value % 1 !== 0)
const emptyStars = computed(() => maxStars - fullStars.value - (hasHalfStar.value ? 1 : 0))


// 유저 리뷰 가져오기

const reviewList = ref([])
const getUserReview = async() => {
  try{
    const response = await publicAxios(`/movies/get-movie-reviews/${props.movie?.id}/`)
    if(response.data.length > 0){
      reviewList.value = response.data
    } else {
      console.log('리뷰가 없습니다.');
    }
  }
  catch(error) {
    console.log('리뷰 로드 중 에러 발생 : ', error)
  }
}

// 사이트 내 영화 통계 가져오기
const movieStats = ref(null)
const fetchMovieStats = async () => {
  try {
    const response = await publicAxios.get(`/movies/get-movie-stats/${props.movie.id}/`)
    movieStats.value = response.data
  } catch (error) {
    console.error('영화 통계 데이터를 가져오는 중 에러 발생:', error)
  }
}


// 유튜브 영상 아이디 가져오는 로직
const youtube_path = ref('')
const findVideoPath = async () => {
  try {
    const response = await publicAxios.get(
      `http://api.themoviedb.org/3/movie/${props.movie?.id}/videos`,
      {
        params: {
          api_key: import.meta.env.VITE_MOVIE_API_KEY,
        },
      }
    )
    const filteredResults = response.data.results.filter(
      (video) => video.type === 'Trailer' && video.size >= 1080
    )

    if (filteredResults.length > 0) {
      youtube_path.value = filteredResults[0].key
      initializePlayer()
    } else {
      console.warn('No suitable trailer found.')
    }
  } catch (error) {
    console.error('유튜브 비디오 패스를 가져오는 중 에러 발생:', error)
  }
}

// 유튜브 API 로드
const player = ref(null)
const loadYouTubeIframeAPI = () => {
  return new Promise((resolve) => {
    const existingScript = document.querySelector('script[src="https://www.youtube.com/iframe_api"]')
    if (!existingScript) {
      const tag = document.createElement('script')
      tag.src = 'https://www.youtube.com/iframe_api'
      document.body.appendChild(tag)

      window.onYouTubeIframeAPIReady = () => {
        resolve(window.YT)
      }
    } else if (window.YT) {
      resolve(window.YT)
    }
  })
}

// 유튜브 플레이어 초기화
const initializePlayer = async () => {
  const YT = await loadYouTubeIframeAPI()

  player.value = new YT.Player('player-container', {
    height: '1500',
    width: '2000',
    videoId: youtube_path?.value,
    playerVars: {
      autoplay: 1,
      mute: 1,
      controls: 0,
      modestbranding: 1,
      rel: 0,
      start: 7,
    },
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  })
}

const onPlayerStateChange = (event) => {
  if (event.data === YT.PlayerState.ENDED) {
    player.value.seekTo(6)
    player.value.playVideo()
  }
}

const onPlayerReady = (event) => {
  event.target.mute()
  event.target.playVideo()
}

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

const genreNames = ref([])

const flattenGenreIds = (genreIds) => {
  if (Array.isArray(genreIds) && genreIds.length > 0 && typeof genreIds[0] === 'object') {
    return genreIds.map(genre => genre.id)
  }
  return genreIds
}

onMounted(() => {
  const genreIds = flattenGenreIds(props.movie.genre_ids)
  genreNames.value = genreIds.map(genreId => store.getGenreNameById(genreId))

  findVideoPath()
  getUserReview()
  fetchMovieStats()
})


</script>

<style scoped>
.modal-overlay {
  position: fixed;
  display: flex;
  flex-direction: column;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: flex-start;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background:  rgba(0, 0, 0, 0.9);
  padding: 0;
  width: 60%;
  height: 100%;
  min-width: 1200px;
  max-width: 1500px;
  min-height: 600px;
  max-height: 1600px;
  text-align: center;
}

.modal-top {
  width: 100%;
  min-width: 1200px;
  max-width: 1500px;
  height: 50vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.modal-top > div > h1 {
  position: absolute;
  color: #f8f8f8;
  z-index: 40000;
  text-align: center;
  top: 40%;
  left: 40%;
  text-shadow: 1px 1px 1px #1f1f1f;
}

.modal-bottom {
  width: 100%;
  height: 50vh;
  min-width: 1200px;
  max-width: 1500px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

iframe {
  width: 1500px;
  height: 1000px;
}

.modal-bleft {
  height: 100%;
  width: auto;
}

.modal-bleft > img {
  height: 100%;
  object-fit: cover;
}

.modal-bright {
  color: #f8f8f8;
  padding: 30px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.detail-title {
  width: 100%;
  text-align: center;
}

.movie-desc {
  width: 100%;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0px;
  gap:30px;
}

.movie-rating {
  display: flex;
  justify-content: center;
  align-items: center;
}

.star {
  width: 20px;
  height: 20px;
  margin-right: 2px;
}

.movie-overview {
  background-color: rgba(248, 248, 248, 0.5);
  border-radius: 10px;
  padding: 20px;
  height: 100px;
  overflow-y: scroll;
  color: #1f1f1f;
}

.movie-overview > p {
  width: 100%;
  padding: 0px 20px;
  line-height: 1.6;
  font-size: 1rem;
  text-align: justify;
  text-wrap: wrap;
  word-break: break-all;
}

.user-reaction {
  margin-top: 30px;
  padding: 20px;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.user-review {
  width: 100%;
  gap:20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.review-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.movie-stats {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.stat-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap:40px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap:10px;
}
.stat-icon {
  width: 40px;
  height: 40px;
}

.close-btn {
  position: absolute;
  top: 50%;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

</style>
