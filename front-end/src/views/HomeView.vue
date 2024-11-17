<template>
  <div class="home-main">
    <div class="home-title">
      <h1>CINEMATE에서 다양한 영화들을 만나보세요!</h1>
    </div>
    <MovieList :movies="store.topMovies" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { onBeforeRouteUpdate } from 'vue-router'
import MovieList from '@/components/movies/MovieList.vue'

// Pinia 스토어 사용
const store = useCounterStore()

// 영화 데이터 로드
const loadMovies = async () => {
  try {
    await store.loadTopMovies()
  } catch (error) {
    console.error('영화 데이터를 로드하는 중 오류 발생:', error)
  }
}

onMounted(() => {
  loadMovies()
})


</script>

<style scoped>
.home-main {
  width: 80%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 50px;
}

.home-title {
  text-align: center;
}
</style>
