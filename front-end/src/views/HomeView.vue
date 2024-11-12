<template>
  <main>
    <h1>Top Rated Movies</h1>
    <ul>
      <MovieListItem v-for="movie in movies" :key="movie.id" :movie="movie" />
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MovieListItem from '@/components/MovieListItem.vue'
import axios from '@/axios'  // 기본 URL 설정된 axios 사용

const movies = ref([])

onMounted(async () => {
  const isMoviesLoaded = localStorage.getItem('movies_loaded')

  if (!isMoviesLoaded) {
    try {
      const loadResponse = await axios.get('/movies/load-top-list/')
      if (loadResponse.data.success) {
        localStorage.setItem('movies_loaded', 'true')
      }
    } catch (error) {
      if (error.response && error.response.status === 400) {
        console.log("영화 데이터가 이미 존재합니다.")
        localStorage.setItem('movies_loaded', 'true')
      } else {
        console.error("영화 데이터를 불러오는 중 오류 발생:", error)
      }
    }
  }
  try {
    const response = await axios.get('/movies/')
    movies.value = response.data
    console.log("불러온 영화 데이터:", movies.value)
  } catch (error) {
    console.error("영화 데이터를 불러오는 중 오류 발생:", error)
  }
})

</script>
