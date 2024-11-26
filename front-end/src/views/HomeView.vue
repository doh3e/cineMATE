<template>
  <div class="home-main">
    <div class="section top-section">
      <h1 class="yesteryear-regular h1-cali">🌘Top Rated Movie</h1>
      <h2 class="subtitle">명작을 보고싶다면…</h2>
      <MovieList :movies="movies" />
    </div>

    <div class="section row-section">
      <!-- 최신 개봉 영화 -->
      <div class="sub-section new-released">
        <h2 class="section-title">국내 최신 개봉 영화</h2>
        <h2 class="section-subtitle">기준일 : {{ today }}</h2>
        <div class="new-container">
          <img
            src="@/assets/img/loading-spinner-unscreen.gif"
            alt="spinner"
            class="loading-spinner"
            v-if="newReleased.length === 0"
          />
          <div
            class="new-item"
            v-else
            v-for="(newr, index) in newReleased"
            :key="newr.index"
            :class="{ active: index === newReleasedIndex }"
          >
            <h3>new!</h3>
            <div class="item-inside">
              <h3 class="item-movietitle">{{ newr.movieNm }}</h3>
              <p class="item-moviedate">{{ formatDate(newr.openDt) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 박스오피스 -->
      <div class="sub-section popular-review">
        <h2 class="section-title">국내 박스오피스 순위</h2>
        <h2 class="section-subtitle">기준일 : {{ yesterday }}</h2>
        <div class="boxoffice-container">
          <img
            src="@/assets/img/loading-spinner-unscreen.gif"
            alt="spinner"
            class="loading-spinner"
            v-if="boxOffices.length === 0"
          />
          <div
            class="boxoffice-item"
            v-else
            v-for="(box, index) in boxOffices"
            :key="box.rnum"
            :class="{ active: index === boxOfficeIndex }"
          >
            <h1>{{ box.rnum }}</h1>
            <div class="item-inside">
              <h3 class="item-movietitle">{{ box.movieNm }}</h3>
              <p>누적관객 {{ box.audiAcc }} 명</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, computed, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import MovieList from '@/components/movies/MovieList.vue'

const store = useCounterStore()

const movies = computed(() => store.topMovies)
const boxOffices = ref([])
const newReleased = ref([])
const KOFIC_API_KEY = import.meta.env.VITE_KOFIC_API_KEY


// 날짜 관련 변수 및 함수
const today = new Date()
const yesterday = new Date(today)
yesterday.setDate(yesterday.getDate() - 1)

const formattedYesterday = yesterday.toISOString().slice(0, 10).replace(/-/g, '')

const formatDate = (dateString) => {
  if (!dateString || dateString.length !== 8) return ''
  const year = dateString.slice(0, 4)
  const month = dateString.slice(4, 6)
  const day = dateString.slice(6, 8)
  return `${year}년 ${month}월 ${day}일`
};

// 인덱스를 통한 애니메이션 상태 관리
const newReleasedIndex = ref(0)
const boxOfficeIndex = ref(0)

const callBoxOffices = async () => {
  try {
    const response = await axios.get(`http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=${KOFIC_API_KEY}&targetDt=${formattedYesterday}`)

    boxOffices.value = response?.data.boxOfficeResult.dailyBoxOfficeList
    console.log(boxOffices.value)
  }
  catch(error) {
    console.error('국내 박스오피스 데이터를 로드하는 중 오류 발생: ', error)
  }
}

const callNewestMovies = async() => {
  try {
    const response = await axios.get(`http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=${KOFIC_API_KEY}&itemPerPage=100&openStartDt=${today.getFullYear()}`)
    const movieList = response?.data.movieListResult.movieList
    const formattedToday = today.toISOString().slice(0, 10).replace(/-/g, '')

    const sortedMovies = movieList
    .filter(movie => movie.openDt)
    .filter(movie => movie.genreAlt !== '성인물(에로)')
    .filter(movie => 
      !(
        movie.nationAlt === '일본' &&
        movie.genreAlt && movie.genreAlt.includes('멜로')
      )
    )
    .filter(movie => movie.openDt <= formattedToday)
    .sort((a, b) => b.openDt.localeCompare(a.openDt))
    .slice(0, 20)
    newReleased.value = sortedMovies
  }
  catch(error) {
    console.error('국내 최신작 데이터를 로드하는 중 오류 발생: ', error)
  }
}

// 항목 순차 전환
const startScrolling = (list, currentIndexRef, interval) => {
  setInterval(() => {
    currentIndexRef.value = (currentIndexRef.value + 1) % list.value.length
  }, interval)
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
  callNewestMovies()
  startScrolling(newReleased, newReleasedIndex, 3000)
  startScrolling(boxOffices, boxOfficeIndex, 3000)
})


</script>

<style scoped>
.home-main {
  width: 80%;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.top-section {
  height: 60vh;
  gap: 20px;
}

.row-section {
  height: 25vh;
  gap: 30px;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.subtitle {
  text-align: center;
  font-family: 'S-CoreDream';
  font-weight: 400;
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
  font-family: 'S-CoreDream';
  font-weight: 600;
  font-size: 1.5rem;
  color: #f8f8f8;
  margin-bottom: 10px; 
}

.section-subtitle{
  text-align: center;
  font-family: 'S-CoreDream';
  font-weight: 200;
  font-size: 1rem;
  font-weight: 400;
  color: #f8f8f8;    
}

.boxoffice-container,
.new-container {
  position: relative;
  width: 100%;
  height: 10vh;
  border-radius: 10px;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  position: relative;
  overflow: hidden;
  margin-top: 15px;
  padding: 20px;
}

.boxoffice-item,
.new-item {
  position: absolute;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  top: 8px;
  width: 100%;
  text-align: center;
  opacity: 0;
  transform: translateY(100%);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.new-item {
  top: 26px;  
}

.boxoffice-item > h1 {
  width: 20%;
  text-align: right;
  font-family: 'S-CoreDream'; 
}

.new-item > h3 {
  width: 25%;
  text-align: right;
  font-family: 'S-CoreDream';
  color: rgb(227, 85, 24);
}

.new-item.active,
.boxoffice-item.active {
  opacity: 1;
  transform: translateY(0);
}

.item-inside {
  width: 100%;
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  font-family: 'S-CoreDream';
}

.item-movietitle {
  width: 80%;
  white-space: nowrap;
  word-wrap: break-word;
  overflow: hidden;
  text-overflow: ellipsis;
}

.movielist-box {
  max-height: 600px;
}

@media screen and (max-width: 700px) {
  .new-released {
    display: none;
  }
}
</style>
