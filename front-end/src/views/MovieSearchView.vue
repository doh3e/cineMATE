<template>
  <div class="movie-container">
    <h1 class="yesteryear-regular h1-cali">🌘Search</h1>
    <div class="movie-head">
      <div class="search-box">
        <input
          v-model="keyword"
          type="text"
          placeholder="검색어를 입력하세요"
          @keyup.enter="searchMovies"
        />
        <button @click="searchMovies">검색</button>
      </div>
    </div>
    <div class="movie-body">
      <div class="tooltip-box" v-if="!isSearched">
          <h3>검색 방법</h3><br>
          <p>원하시는 영화의 제목을 2글자 이상 입력해주세요.</p>
          <p>띄어쓰기를 정확히 하셔야 해요. (ex.세얼간이x 세 얼간이o)</p>
          <p>영문명으로도 검색이 가능합니다.</p>
      </div>
      <div class="tooltip-box" v-if="isSearched && movies.length === 0">
          <h3>❓ 검색 결과가 없습니다 ❓</h3><br>
          <p>검색어를 한 번 더 확인해주세요!</p>
          <p>띄어쓰기가 틀렸을 경우 검색에 나오지 않을 수 있습니다.</p>
      </div>
      <div class="result-box">
        <MovieSearch
          v-if="isSearched"
          :movies="movies"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MovieSearch from '@/components/movies/MovieSearch.vue'
import { authAxios, publicAxios } from '@/axios'

const movies = ref([]) // 검색 결과
const keyword = ref('') // 검색 키워드
const isSearched = ref(false) // 검색 여부 상태

// 검색 실행
const searchMovies = async () => {
  if (!keyword.value.trim()) {
    alert('검색 키워드를 입력해주세요!')
    return
  }

  if (keyword.value.length < 2) {
    alert('검색어는 두 글자 이상 입력해주세요!')
    return
  }

  movies.value = []

  try {
    const response = await publicAxios.get('/movies/search/', {
      params: { query: keyword.value.trim() },
    })
    movies.value = response.data
    isSearched.value = true
  } catch (error) {
    console.error('검색 중 오류 발생:', error)
  }
}


</script>

<style scoped>
.movie-container {
  width: 80%;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

.movie-head {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  min-width: 300px;
  max-width: 600px;
  display: flex;
  gap: 10px;
}

.search-box > input[type=text]{
  height: 3rem;
  width: 80%;
  min-width: 200px;
  max-width: 500px;
  padding: 10px 20px;
  text-align: center;
  font-size: 1.3rem;
  font-weight: 600;
}

.movie-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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

.search-box button {
  padding: 10px 20px;
  height: 3rem;
  min-width: 80px;
  background-color: #7469B6;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-box button:hover {
  background-color: #574F9F;
}

.result-box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
