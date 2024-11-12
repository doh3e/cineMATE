<!-- src/components/MovieListItem.vue -->
<template>
  <li class="movie-item">
    <h3>{{ movie.movie_title }}</h3>
    <p>{{ movie.movie_overview }}</p>
    <p>Rating: {{ movie.movie_rating }}</p>
    <img :src="getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path">
  </li>
</template>

<script setup>
const props = defineProps({
  movie: Object,
})

// getImageUrl 함수를 직접 선언
function getImageUrl(path) {
  return `https://image.tmdb.org/t/p/w500${path}`
}
</script>

<style scoped>
.movie-item {
  margin: 10px 0;
}
</style>
