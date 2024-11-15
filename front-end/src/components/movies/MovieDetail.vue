<template>
  <div v-if="movie && isVisible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">X</button>
      <h2>{{ movie.movie_title }}</h2>
      <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
      <p>평점: {{ movie.movie_rating }}</p>
      <p>장르: {{ genreNames.join(', ') }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { computed, watch, ref } from 'vue';

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

const genreNames = computed(() => {
  return props.movie.genres.map(genre => store.getGenreNameById(genre.id))
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
  text-align: center;
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
