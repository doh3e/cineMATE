<template>
  <div class="curation-container">
    <h1>더욱 심화된 큐레이션</h1>

    <!-- 생일 추천 영화 -->
    <div class="curation-title" v-if="isBirthday && birthDayQue.length > 0">
      <h3>🎉 생일 축하해요, {{ store.userInfo?.nickname }}님! 🎉</h3>
      <p> 당신이 태어난 해에 개봉한 영화들을 보여줄게요. </p>
    </div>
    <MovieCurationList
      v-if="isBirthday && birthDayQue.length > 0"
      :movies="birthDayQue"
    />

    <!-- 특별한 날 추천 영화 -->
    <div class="curation-title" v-if="isEventDay && eventDayQue.length > 0">
      <h3>오늘은 {{ currentSpecialDay }}!</h3>
      <p> {{ eventMent }} </p>
    </div>
    <MovieCurationList
      v-if="isEventDay && eventDayQue.length > 0"
      :movies="eventDayQue"
    />
    <!-- 기본 추천 영화 -->
    <div class="curation-title" v-if="defaultQue.length > 0">
      <h3>선호하시는 장르의 영화를 찾아봤어요!</h3>
    </div>
    <MovieCurationList
      v-if="defaultQue.length > 0"
      :movies="defaultQue"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter'
import MovieCurationList from '@/components/movies/MovieCurationList.vue'

const store = useCounterStore()

// 상태 관리
const isBirthday = ref(false) // 생알 여부
const isEventDay = ref(false) // 특별한 날 여부
const currentSpecialDay = ref('') // 현재 특별한 날 (생일/이벤트 이름)
const eventMent= ref('')

// 추천 영화
const birthDayQue = ref([]) // 생일 영화 추천
const eventDayQue = ref([]) // 특별한 날 영화 추천
const defaultQue = ref([]) // 기본 추천 영화 리스트


// 기본 추천 영화 로드 (좋아요, 북마크에 따른)
const loadRecommendations = async () => {
  try {
    const response = await authAxios.get('/movies/recommend/default/')
    defaultQue.value = response.data
  } catch (error) {
    console.error('추천 영화 로드 중 오류 발생:', error)
  }
}

// 특별한 날(크리스마스, 할로윈 등)
const eventDay = {
  '01-01': ['새해', `${store.userInfo?.nickname}님, 새해에는 어떤 다짐을 하셨나요?`],
  '01-29': ['설날', '명절에 가족들과 함께 볼 수 있는 영화들을 소개할게요.'],
  '02-14': ['발렌타인데이', '사랑하는 사람과의 달콤한 시간을 누려요.'],
  '03-01': ['삼일절', '역사를 잊은 민족에게 미래는 없습니다.'],
  '03-14': ['화이트데이', '사랑하는 사람과의 달콤한 시간을 누려요.'],
  '05-05': ['어린이날', '오월은 푸르고 어린이들이 자라나는 달입니다.'],
  '05-08': ['어버이날', '키워주신 감사를 전해봐요.'],
  '08-15': ['광복절', '역사를 잊은 민족에게 미래는 없습니다.'],
  '10-06': ['추석', '명절에 가족들과 함께 볼 수 있는 영화들을 소개할게요.'],
  '10-31': ['할로윈', '할로윈이니 으스스한 영화 어때요?'],
  '11-19': ['프로젝트 발표연습', '프로젝트를 위해 머리를 잔뜩 굴려볼까요?'],
  '11-27': ['프로젝트 발표날', '프로젝트를 위해 머리를 잔뜩 굴려볼까요?'],
  '12-24': ['크리스마스 이브', '이번 크리스마스엔 무엇을 하시나요?'],
  '12-25': ['크리스마스', `메리 크리스마스, ${store.userInfo?.nickname}님!`],
  '12-31': ['연말'],
}

// 날짜 비교 함수
const isToday = (date) => {
  const today = new Date()
  const [year, month, day] = date.split('-')
  console.log(year, month, day)
  return today.getMonth() + 1 === parseInt(month) && today.getDate() === parseInt(day)
}

// 생일 및 특별한 날 체크
const checkSpecialDay = () => {
  const todayKey = new Date().toISOString().slice(5, 10) // 'MM-DD'
  const userBirthday = store.userInfo?.birthday

  // 생일 체크
  if (userBirthday && isToday(userBirthday)) {
    isBirthday.value = true
    currentSpecialDay.value = '생일'
  }

  // 특별한 날 체크
  if (eventDay[todayKey]) {
    isEventDay.value = true
    currentSpecialDay.value = eventDay[todayKey][0]
    eventMent.value = eventDay[todayKey][1]
  }
}

// 생일 영화 API 호출
const fetchBirthdayMovies = async () => {
  try {
    const response = await authAxios.get('/movies/recommend/birthday/')
    birthDayQue.value = response.data
    console.log('생일 추천 영화:', birthDayQue.value)
  } catch (error) {
    console.error('생일 영화 추천 API 호출 중 오류 발생:', error)
  }
}

// 특별한 날 영화 API 호출
const fetchEventDayMovies = async () => {
  try {
    const params = { keyword: currentSpecialDay.value }
    const response = await authAxios.get('/movies/recommend/eventday/', { params })
    eventDayQue.value = response.data
    console.log('특별한 날 추천 영화:', eventDayQue.value)
  } catch (error) {
    console.error('특별한 날 영화 추천 API 호출 중 오류 발생:', error)
  }
}

onMounted(() => {
  loadRecommendations()
  checkSpecialDay()
  if (isBirthday.value) fetchBirthdayMovies()
  if (isEventDay.value) fetchEventDayMovies()
})



</script>

<style scoped>
.curation-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>
