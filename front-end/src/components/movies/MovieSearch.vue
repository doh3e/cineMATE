<template>
  <div class="result-list" v-if="movies.length > 0">
      <MovieList
        :movies="movies"
        :hasMore="hasMore"
        @loadMore="loadMoreSearchMovies"
      />
  </div>
  <div v-else>
      <h3>
        {{ isSearched ? "검색 결과가 없습니다. 다른 검색어를 입력해보세요!" : "검색어를 입력하고 영화를 찾아보세요!" }}
      </h3>
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
.search-box {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-box input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-box button {
  padding: 10px 20px;
  background-color: #7469B6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-box button:hover {
  background-color: #574F9F;
}

.result-list {
  margin-top: 20px;
}
</style>
