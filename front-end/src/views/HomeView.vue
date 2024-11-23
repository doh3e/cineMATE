<template>
  <div class="home-main">

    <div class="section">
      <h1 class="yesteryear-regular h1-cali">Top Rated Movie</h1>
      <h2 class="subtitle">명작을 보고싶다면…</h2>
      <MovieList :movies="movies" />
    </div>

    <div class="section row-section">
      <div class="sub-section new-released">
        <h1 class="yesteryear-regular h1-cali">New Released</h1>
        <h2 class="subtitle">스크롤 페이징 처리 해야지!</h2>
        <h2 class="subtitle">스크롤 페이징 처리 해야지!</h2>
        <h2 class="subtitle">스크롤 페이징 처리 해야지!</h2>
      </div>
      <div class="sub-section popular-review">
        <h2 class="section-title">국내 박스오피스 순위</h2>
        <h2 class="section-subtitle">기준일 : {{ yesterday }}</h2>
        <div class="boxoffice-container" v-if="boxOffices.length > 0">
          <span v-for="box in boxOffices" :key="box.rnum">
            {{box.rnum}} {{box.movieNm}}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { onBeforeRouteUpdate } from 'vue-router'
import { useRouter } from 'vue-router'
import MovieList from '@/components/movies/MovieList.vue'
import { publicAxios } from '@/axios'
import axios from 'axios'

const store = useCounterStore()

const movies = computed(() => store.topMovies)
const boxOffices = ref([])
const KOFIC_API_KEY = import.meta.env.VITE_KOFIC_API_KEY
const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1) // 현재 날짜에서 하루 빼기
const formattedYesterday = yesterday.toISOString().slice(0, 10).replace(/-/g, '')

const callBoxOffices = async () => {
  try {
    const response = await axios.get(`http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=${KOFIC_API_KEY}&targetDt=${formattedYesterday}`)

    boxOffices.value = response.data.boxOfficeResult.dailyBoxOfficeList
  }
  catch(error) {
    console.error('국내 박스오피스 데이터를 로드하는 중 오류 발생: ', error)
  }
}

const loadMovies = async () => {
  try {
    await store.loadTopMovies()
  } catch (error) {
    console.error('영화 데이터를 로드하는 중 오류 발생:', error)
  }
}

onMounted(() => {
  loadMovies()
  callBoxOffices()
})


</script>

<style scoped>
.home-main {
  padding-top: 60px;
  width: 80%;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

.section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.row-section {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.h1-cali {
  margin: 0 auto;
  text-align: center;
  vertical-align: middle;
  font-size: 4rem;
  color: #f8f8f8;
}

.subtitle {
  text-align: center;
  font-family: 'S-CoreDream-3Light';
  font-size: 1.2rem;
  color: #f8f8f8;
}

.sub-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.section-title {
  text-align: center;
  font-family: 'S-CoreDream-3Light';
  font-size: 1.5rem;
  color: #f8f8f8;
  margin-bottom: 10px; 
}

.section-subtitle{
  text-align: center;
  font-family: 'S-CoreDream-3Light';
  font-size: 1rem;
  font-weight: 400;
  color: #f8f8f8;    
}

.boxoffice-container {
  width: 100%;
  height: 200px;
  border-radius: 10px;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  padding: 30px;
  gap: 10px;
  overflow-y: scroll;
  margin-top: 20px;
}
</style>
