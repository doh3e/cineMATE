<template>
  <div ref="movielistBox" class="movielist-box">
    <MovieListItem v-for="movie in displayedMovies" :key="movie.id" :movie="movie" />
    <div class="loading" v-if="isLoading || hasMore">
      <img src="@/assets/img/loading-spinner-unscreen.gif" alt="spinner" class="loading-spinner">
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import MovieListItem from './MovieListItem.vue'

const props = defineProps({
  movies: {
    type: Array,
    default: () => [] // 부모 컴포넌트에서 전달받은 전체 영화 데이터
  }
})

const displayedMovies = ref([]) // 화면에 표시할 영화 데이터
const movielistBox = ref(null)
const isLoading = ref(false)
const currentPage = ref(1)
const moviesPerPage = 10 // 한 번에 보여줄 영화 수
const hasMore = ref(true) // 추가 데이터 유무

// 초기화 함수
const resetPagination = () => {
  currentPage.value = 1
  hasMore.value = true
  displayedMovies.value = []
}

// 페이징 처리
const paginateMovies = () => {
  const startIndex = (currentPage.value - 1) * moviesPerPage
  const endIndex = startIndex + moviesPerPage
  const newMovies = props.movies.slice(startIndex, endIndex)

  if (newMovies.length > 0) {
    displayedMovies.value.push(...newMovies)
    currentPage.value += 1
    hasMore.value = displayedMovies.value.length < props.movies.length
  } else {
    hasMore.value = false
  }
}

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  if (!movielistBox.value || isLoading.value || !hasMore.value) return

  const { scrollTop, scrollHeight, clientHeight } = movielistBox.value

  if (scrollTop + clientHeight >= scrollHeight - 50) {
    isLoading.value = true
    setTimeout(() => {
      paginateMovies()
      isLoading.value = false
    }, 500)
  }
}

// 초기 로드
onMounted(() => {
  movielistBox.value = document.querySelector('.movielist-box')
  movielistBox.value?.addEventListener('scroll', handleScroll)
  paginateMovies()
})

onBeforeUnmount(() => {
  movielistBox.value?.removeEventListener('scroll', handleScroll)
})

// 영화 데이터 변경 감지
watch(() => props.movies, (newMovies) => {
  resetPagination()
  paginateMovies()
}, { immediate: true })
</script>

<style scoped>
.movielist-box {
  background-color: #f8f8f8;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 40px;
  width: 100%;
  border-radius: 10px;
  max-height: 1000px;
  margin: 0 auto;
  padding: 40px 40px;
  overflow-y: scroll;
}

.loading {
  text-align: center;
  padding: 1em;
}
</style>
