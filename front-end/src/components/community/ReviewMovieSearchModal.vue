<template>
  <div class="modal">
    <div class="modal-content">
      <h3>영화 검색</h3>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="영화 제목을 입력하세요"
      />
      <button @click="searchMovies">검색</button>
      <div class="result-box">
        <ul v-if="movies && movies.length > 0">
          <li
            v-for="movie in movies"
            :key="movie.id"
            @click="selectMovie(movie)"
            class="movie-item"
          >
            {{ movie.title }} ({{ movie.release_date }})
          </li>
        </ul>
        <div v-else-if="movies.length === 0 && isSearch">
          <h4>검색결과가 없습니다 ㅠ_ㅠ</h4>
        </div>
        <div v-else>
          <h4>키워드를 입력하고 검색하면 리스트가 나옵니다</h4>
          <p>원하는 영화 선택 시 자동으로 리뷰 정보에 등록됩니다.</p>
        </div>
      </div>
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { publicAxios } from '@/axios';

const searchQuery = ref('')
const movies = ref([])
const isSearch = ref(false)

// 영화 검색
const searchMovies = async () => {
  if(searchQuery.value.length < 2){
    alert('검색어는 두 글자 이상 입력해주세요!')
    return
  }
  try {
    const response = await publicAxios.get('/movies/search/', {
      params: { query: searchQuery.value }
    })
    movies.value = response.data
    isSearch.value = true
    console.log(movies)
  } catch (error) {
    console.error('영화 검색 실패:', error)
    movies.value = []
  }
}

const emit = defineEmits(['select'])

// 영화 선택
const selectMovie = (movie) => {
  emit('select', movie)
}
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 450px;
}

.result-box {
  width: 90%;
  max-height: 400px;
  overflow-y: scroll;
}

.movie-item {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #ddd;
  margin: 5px 0;
  border-radius: 5px;
}
.movie-item:hover {
  background-color: #f0f0f0;
}
</style>
