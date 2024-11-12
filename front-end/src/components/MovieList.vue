<!-- src/components/MovieList.vue -->
<template>
  <ul>
    <MovieListItem v-for="movie in movies" :key="movie.id" :movie="movie" />
  </ul>
</template>

<script setup>
import MovieListItem from './MovieListItem.vue'

const props = defineProps({
  movies: Array,
})
</script>

<style scoped>
/* 스타일을 여기에 추가할 수 있습니다 */
</style>
