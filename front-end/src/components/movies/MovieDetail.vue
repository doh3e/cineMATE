<template>
  <div v-if="movie && isVisible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-top">
        <div id="player-container"
        @mouseenter="onPlayerMouseEnter"
        @mouseleave="onPlayerMouseLeave"></div>
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
            </div>
            <div class="etc">
              <h3>여긴 뭐하지</h3>
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
      console.log('YouTube Path:', youtube_path.value)
      initializePlayer()
    } else {
      console.warn('No suitable trailer found.')
    }
  } catch (error) {
    console.error('Error fetching video path:', error)
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
  event.player.mute()
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
  height: 150px;
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
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
