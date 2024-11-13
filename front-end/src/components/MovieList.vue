<!-- src/components/MovieList.vue -->
<template>
  <div class="movielist-box">
    <MovieListItem v-for="movie in movies" :key="movie.id" :movie="movie" />
  </div>
</template>

<script setup>
import MovieListItem from './MovieListItem.vue'

const props = defineProps({
  movies: Array,
})
</script>

<style scoped>
.movielist-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
