<template>
  <div class="result-list" v-if="movies.length > 0">
      <MovieList
        :movies="movies"
        :hasMore="hasMore"
      />
  </div>
</template>
<script setup>
import { ref } from 'vue'
import MovieList from '@/components/movies/MovieList.vue'
import { publicAxios } from '@/axios'

const props = defineProps({
  movies: Array,
  hasMore: Boolean,
})

const emit = defineEmits(['loadMore'])

</script>

<style scoped>

.movielist-box {
  height: 60vh;
  max-height: 880px;
}

</style>
