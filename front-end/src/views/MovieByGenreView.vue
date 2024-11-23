<template>
  <div class="mvbygenre-container">
    <h1 class="yesteryear-regular h1-cali">🌘Genre Movies</h1>
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
    <div class="result-box" v-if="sortedMovies.length > 0">
      <MovieList
        :movies="sortedMovies"
      />
    </div>
    <div v-else class="tooltip-box">
      <h3>장르별 영화 보기</h3><br>
          <p>장르 별 자주 찾는</p>
          <p>띄어쓰기를 정확히 하셔야 해요. (ex.세얼간이x 세 얼간이o)</p>
          <p>영문명으로도 검색이 가능합니다.</p>
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
    case 'latest':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort(
        (a, b) => new Date(b.release_date) - new Date(a.release_date)
      )
      break
    case 'oldest':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort(
        (a, b) => new Date(a.release_date) - new Date(b.release_date)
      )
      break
    case 'title_asc':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => a.title.localeCompare(b.title))
      break
    case 'title_desc':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.title.localeCompare(a.title))
      break
    case 'popularity':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.popularity - a.popularity)
      break
    case 'rating':
      sortedMovies.value = []
      sortedMovies.value = [...movies].sort((a, b) => b.vote_average - a.vote_average)
      break
    default:
      sortedMovies.value = []
      sortedMovies.value = [...movies]
  }
}

watch([genreMovies, selectedOrder], sortMovies)

</script>


<style scoped>
.mvbygenre-container {
  width: 100%;
  padding: 60px;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
}

.select-area {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.select-area > select {
  background-color: #f8f8f8;
  border-radius: 5px;
  width: 15%;
  height: 3rem;
  min-width: 150px;
  max-width: 300px;
  font-family: 'S-CoreDream-3Light';
  font-size: 1.3rem;
  font-weight: 600;
  padding: 5px;
}

.tooltip-box {
  width: 50%;
  max-width: 1000px;
  min-width: 500px;
  padding: 30px 40px;
  background-color: rgba(254, 254, 254, 0.7);
  border-radius: 10px;
  height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.result-box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}


</style>
