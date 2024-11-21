<template>
    <div v-if="displayedMovies.length > 0" class="movielist-box">
      <MovieListItem v-for="movie in displayedMovies" :key="movie.id" :movie="movie" />
    </div>
    <p v-else>영화 데이터를 불러오는 중입니다...</p>
    <div ref="loadMoreTrigger" class="loading">
      <p v-if="isLoading">로딩 중...</p>
      <p v-else-if="hasMore">더 많은 영화를 로드합니다...</p>
      <p v-else>더 이상 데이터가 없습니다.</p>
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
const loadMoreTrigger = ref(null)
const observer = ref(null)
const isLoading = ref(false)
const currentPage = ref(1)
const moviesPerPage = 20 // 한 번에 보여줄 영화 수
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
  } else {
    hasMore.value = false
  }
}

// 무한 스크롤 설정
onMounted(() => {
  paginateMovies()

  observer.value = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !isLoading.value && hasMore.value) {
      paginateMovies()
    }
  })

  if (loadMoreTrigger.value) {
    observer.value.observe(loadMoreTrigger.value)
  }
})

watch(() => props.movies, (newMovies) => {
  resetPagination() // 페이징 초기화
  paginateMovies()  // 첫 페이지 로드
}, { immediate: true })

// 컴포넌트가 언마운트될 때 관찰 중지
onBeforeUnmount(() => {
  if (observer.value && loadMoreTrigger.value) {
    observer.value.unobserve(loadMoreTrigger.value)
  }
})
</script>

<style scoped>

.movielist-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.movielist-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 40px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 1em;
}
</style>
