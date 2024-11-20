<template>
  <div class="movie-container">
    <h1>영화 추천/검색 영역</h1>
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
    <div class="result-box">
      <MovieSearch
        v-if="isSearched"
        :movies="movies"
        :hasMore="hasMore"
        @loadMore="loadMoreSearchMovies"
      />
    </div>
    <div class="desciprtion-box" v-if="!isSearched">
      <h3>검색 방법</h3>
      <p>원하시는 영화의 제목을 2글자 이상 입력해주세요.</p>
      <p>띄어쓰기를 정확히 하셔야 해요. (ex.세얼간이x 세 얼간이o)</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MovieSearch from '@/components/movies/MovieSearch.vue'
import { authAxios, publicAxios } from '@/axios'

const movies = ref([]) // 검색 결과
const hasMore = ref(false) // 추가 데이터 유무
const keyword = ref('') // 검색 키워드
const currentPage = ref(1) // 현재 페이지
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
  hasMore.value = false
  currentPage.value = 1

  try {
    const response = await publicAxios.get('/movies/search/', {
      params: { query: keyword.value.trim() },
    })

    movies.value = response.data
    hasMore.value = movies.value.length > 20
    currentPage.value = 1
    isSearched.value = true
  } catch (error) {
    console.error('검색 중 오류 발생:', error)
  }
}

// 추가 검색 결과 로드
const loadMoreSearchMovies = async () => {
  try {
    const nextPage = currentPage.value + 1
    const response = await publicAxios.get('/movies/search/', {
      params: { query: keyword.value.trim(), page: nextPage },
    })

    const newMovies = response.data
    movies.value = [...movies.value, ...newMovies]
    hasMore.value = newMovies.length > 0
    currentPage.value = nextPage
  } catch (error) {
    console.error('추가 검색 중 오류 발생:', error)
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
  justify-content: center;
  align-items: center;
  gap: 30px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
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

.result-box {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
