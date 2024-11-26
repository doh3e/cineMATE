<template>
  <div class="modal">
    <div class="modal-content">
      <h2 class="modal-title">영화 검색</h2>
      <div class="searchbar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="영화 제목을 입력하세요"
          @keyup.enter.prevent="searchMovies"
          id="searchbar"
        />
        <button @click="searchMovies">검색</button>
      </div>
      <div class="result-box">
        <div v-if="movies && movies.length > 0"
            v-for="movie in movies"
            :key="movie.id"
            @click="selectMovie(movie)"
            class="movie-item"
          >
            <img :src="store.getImageUrl(movie.poster_path)" alt="poster" v-if="movie.poster_path">
            <img src="@/assets/img/default_movie_poster.png" alt="poster" v-else>
            <div class="info-box"><p>{{ movie.title }}</p>
              <p>({{ movie.release_date ? movie.release_date.slice(0, 4) : 'N/A' }})</p>
            </div>
        </div>
        <div class="info" v-else-if="movies.length === 0 && isSearch">
          <h4>검색결과가 없습니다 ㅠ_ㅠ</h4>
        </div>
        <div v-else class="info">
          <h3>키워드를 입력하고 검색하면 리스트가 나옵니다!</h3>
          <p>원하는 영화 선택 시 자동으로 리뷰 정보에 등록됩니다.</p>
        </div>
      </div>
      <button @click="$emit('close')" class="close-btn">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { publicAxios } from '@/axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
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
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: rgba(248, 248, 248, 1);
  padding: 30px;
  width: 100%;
  min-width: 400px;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap:20px;
}

.modal-title{
  font-family: 'S-CoreDream';
  font-weight: 600;
}

.searchbar {
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap:10px;
}

#searchbar {
  width: 70%;
  height: 35px;
  padding: 5px;
}

.searchbar > button {
  height: 35px;
  width: 15%;
  cursor: pointer;
}

.result-box {
  width: 90%;
  height: 100%;
  min-height: 200px;
  max-height: 400px;
  overflow-y: scroll;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.movie-item {
  flex: 1 1 calc(33.333% - 10px);
  max-width: calc(33.333% - 10px);
  height: 100%;
  cursor: pointer;
  background-color: #ddd;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 5px;
  gap: 5px;
}

@media (max-width: 1024px) {
  .movie-item {
    flex: 1 1 calc(50% - 10px);
    max-width: calc(50% - 10px);
  }
}

@media (max-width: 768px) {
  .movie-item {
    flex: 1 1 calc(100% - 10px);
    max-width: calc(100% - 10px);
  }
}

.info-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  word-wrap: break-word;
  width: 90%;
  font-size: 0.9rem;
}

.movie-item:hover {
  background-color: #999;
}

.movie-item > img {
  width: 50px;
}

.close-btn {
  height: 35px;
  width: 15%;
  cursor: pointer;
}

.info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
