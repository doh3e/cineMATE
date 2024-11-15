<!-- src/components/MovieListItem.vue -->
<template>
  <div class="movie-item" @click="openModal">
    <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
    <h4>{{ movie.movie_title }} ({{ movie.movie_rating }})</h4>
  </div>

  <MovieDetail
    v-if="movie && isModalVisible"
    :movie="movie"
    :isVisible="isModalVisible"
    @close="closeModal"
  />
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCounterStore } from '@/stores/counter';
import MovieDetail from './MovieDetail.vue'

const store = useCounterStore()

defineExpose({
  store
})

const props = defineProps({
  movie: Object,
})

const isModalVisible = ref(false)

const openModal = () => { 
  isModalVisible.value = true
}

const closeModal = () => {
  isModalVisible.value = false
}

</script>

<style scoped>
.movie-item {
  flex: 1 1 200px;
  max-width: 220px;
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
