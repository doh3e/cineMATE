<template>
  <div class="movie-item" @click="showDetail">
    <img :src="store.getImageUrl(movie.poster_path)" alt="poster" class="poster">
    <div class="overlay">
      <p class="title">{{ movie.title }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const props = defineProps({
  movie: Object
})

const emit = defineEmits(['showDetail']);

const showDetail = () => {
  emit('showDetail', props.movie);
};

</script>

<style scoped>

.movie-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  border-radius: 10px;
  transition: transform 0.4s ease;
}

.poster {
  width: 100%;
  height: 100%;
  aspect-ratio: 1/1;
  object-fit: cover;
  transition: transform 0.4s ease, filter 0.4s ease;
}

.movie-item:hover {
  transform: scale(1.1);
}

.movie-item:hover .poster {
  filter: brightness(0.8);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.movie-item:hover .overlay {
  opacity: 1;
}

.title {
  color: white;
  font-size: 1rem;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}
</style>
