<template>
  <div v-if="movie && isVisible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">X</button>
      <h2 class="truncate">{{ movie.title }}</h2>
      <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
      <img v-else src="@/assets/img/default_movie_poster.png" alt="Default Poster" id="movie-poster">
      <p>평점: {{ movie.vote_average }}</p>
      <p>장르: {{ genreNames.join(', ') }}</p>
      <p>{{ movie.overview }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { computed, watch, ref, onMounted } from 'vue';

const store = useCounterStore();

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close')
}

const genreNames = ref([])

const flattenGenreIds = (genreIds) => {
  if (Array.isArray(genreIds) && genreIds.length > 0 && typeof genreIds[0] === 'object') {
    return genreIds.map(genre => genre.id)
  }
  return genreIds
}

onMounted(() => {
  const genreIds = flattenGenreIds(props.movie.genre_ids)
  genreNames.value = genreIds.map(genreId => store.getGenreNameById(genreId))
})


</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.modal-content {
  position: relative;
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
  min-width: 350px;
  height: 90vh;
  min-height: 450px;
  text-align: center;
  overflow-y: scroll;
}

.modal-content > img {
  width: 90%;
  min-width: 300px;
  object-fit: cover;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

</style>
