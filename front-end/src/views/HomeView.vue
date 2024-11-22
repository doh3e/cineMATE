<template>
  <div class="home-main">
    <h1 class="yesteryear-regular h1-cali">Top Rated Movie</h1>
    <MovieList :movies="movies" />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { onBeforeRouteUpdate } from 'vue-router'
import { useRouter } from 'vue-router'
import MovieList from '@/components/movies/MovieList.vue'

const store = useCounterStore()

const movies = computed(() => store.topMovies)

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

.h1-cali {
  padding-top: 80px;
  margin: 0 auto;
  text-align: center;
  vertical-align: middle;
  font-size: 6rem;
  color: #f8f8f8;
}
</style>
