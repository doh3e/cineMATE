<!-- src/components/MovieListItem.vue -->
<template>
  <div class="movie-item">
    <img :src="getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
    <h4>{{ movie.movie_title }} ({{ movie.movie_rating }})</h4>
  </div>
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
  flex: 1 1 200px; /* 기본 너비를 200px로 설정하고 공간에 맞게 늘어남 */
  max-width: 220px; /* 최대 너비 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  box-sizing: border-box;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

#movie-poster {
  width: 200px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 4px;
}
</style>
