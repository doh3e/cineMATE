<template>
  <div v-if="movie && isVisible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-top">
        <iframe :src="videoLink" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
      <div class="modal-bottom">
        <div class="modal-bleft">
          <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
          <img v-else src="@/assets/img/default_movie_poster.png" alt="Default Poster" id="movie-poster">
        </div>
        <div class="modal-bright">
          <h2 class="truncate">{{ movie.title }}</h2>
          <p>평점: {{ movie.vote_average }}</p>
          <p>장르: {{ genreNames.join(', ') }}</p>
          <p>{{ movie.overview }}</p>
        </div>
      </div>
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

const videoLink = computed(() => {
  return props.movie?.youtube_path
    ? `https://www.youtube-nocookie.com/embed/${props.movie.youtube_path}?si=CB1jacN09Ik4Tkbp&controls=0&start=6&modestbranding=1&rel=0&autoplay=1&disablekb=1&fs=0&loop=1&mute=1`
    : ''
})

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
  display: flex;
  flex-direction: column;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-start;
  align-items: center;
  z-index: 9999;
}
.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.8);
  padding: 0;
  width: 60%;
  height: 100vh;
  min-width: 350px;
  min-height: 450px;
  text-align: center;
}

.modal-top,
.modal-bottom {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

iframe {
  width: 100%;
  height: 60vh;
}

.modal-bleft > img {
  height: 50vh;
  object-fit: cover;
}

.modal-bright {
  color: #f8f8f8;
  padding: 30px;
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
