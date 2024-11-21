<template>
  <div class="mvbygenre-container">
    <h1>장르별 보기 페이지</h1>
    <div class="select-area">
      <!-- 장르 선택 -->
      <select v-model="selectedGenre" @change="fetchGenreMovies">
        <option value="" disabled>장르를 선택하세요</option>
        <option 
          v-for="(name, id) in GENRE_MAP" 
          :key="id" 
          :value="id"
        >
          {{ name }}
        </option>
      </select>

      <!-- 정렬 선택 -->
      <select v-if="genreMovies.length > 0" v-model="selectedOrder" @change="sortMovies">
        <option value="" selected>기본순</option>
        <option value="latest">최신순</option>
        <option value="oldest">오래된 순</option>
        <option value="title_asc">이름순</option>
        <option value="title_desc">이름역순</option>
        <option value="popularity">인기순</option>
        <option value="rating">평점순</option>
      </select>
    </div>

    <!-- 영화 목록 -->
    <MovieList
      v-if="sortedMovies.length > 0"
      :movies="sortedMovies"
    />
    <div v-else>
      <h3>장르를 선택하세요!</h3>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue'
import { useCounterStore } from '@/stores/counter';
import MovieList from '@/components/movies/MovieList.vue';
import { publicAxios } from '@/axios';

const store = useCounterStore()
const GENRE_MAP = store.GENRE_MAP

// 상태값
const selectedGenre = ref('')
const genreMovies = ref([])
const selectedOrder = ref('')
const sortedMovies = ref([])

// 선택된 장르의 영화 가져오기
const fetchGenreMovies = async () => {
  if (!selectedGenre.value) {
    genreMovies.value = []
    return
  }
  try {
    genreMovies.value = []
    const response = await publicAxios.get(`/movies/movie-by-genre/${selectedGenre.value}/`)
    genreMovies.value = response.data
  } catch (error) {
    console.error('영화 데이터를 불러오지 못했습니다:', error)
  }
}

// 정렬 처리 로직
const sortMovies = () => {
  const movies = [...genreMovies.value]
  switch (selectedOrder.value) {
    case 'latest': // 최신순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort(
        (a, b) => new Date(b.release_date) - new Date(a.release_date)
      )
      break
    case 'oldest': // 오래된 순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort(
        (a, b) => new Date(a.release_date) - new Date(b.release_date)
      )
      break
    case 'title_asc': // 이름순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => a.title.localeCompare(b.title))
      break
    case 'title_desc': // 이름 역순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.title.localeCompare(a.title))
      break
    case 'popularity': // 인기순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.popularity - a.popularity)
      break
    case 'rating': // 평점순
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.vote_average - a.vote_average)
      break
    default: // 기본순
      sortedMovies.value = []
      sortedMovies.value = [...movies]
  }
}

watch([genreMovies, selectedOrder], sortMovies)

</script>


<style scoped>
.mvbygenre-container {
  padding: 20px;
}

.select-area {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

select {
  padding: 5px;
}
</style>
