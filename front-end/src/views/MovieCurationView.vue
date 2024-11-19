<template>
  <div class="curation-container">
    <h1>더욱 심화된 큐레이션</h1>
    <MovieCurationList
      v-if="isBirthday && birthDayQue.length > 0"
      :movies="birthDayQue"
    />
    <MovieCurationList
      v-if="isEventDay"
    />
    <MovieCurationList/>
    <MovieCurationList/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { publicAxios, authAxios } from '@/axios';
import { useCounterStore } from '@/stores/counter';
import MovieCurationList from '@/components/movies/MovieCurationList.vue';

const store = useCounterStore()
const isBirthday = ref(false)
const isEventDay = ref(false)
const birthDayQue = ref([])

// 생일 영화 추천 로직
const isValidBirthday = (birthday) => {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(birthday)) {
    return false;
  }

  const date = new Date(birthday);
  return date instanceof Date && !isNaN(date);
}

const checkBirthday = () => {
  const userBirthday = store.userInfo?.birthday
  if (!userBirthday || !isValidBirthday(userBirthday)) return false

  const today = new Date()
  const [year, month, day] = userBirthday.split('-')

  return today.getMonth() + 1 === parseInt(month) && today.getDate() === parseInt(day)
}

const birthdayMovie = async () => {
  if (!isBirthday.value) {
    console.log('생일 아님!')
    return
  }

  try {
    const response = await authAxios.get('/movies/recommend/birthday/')
    birthDayQue.value = response.data
    console.log(birthDayQue.value)
  } catch (error) {
    console.log('생일 추천 영화 로드 중 오류 발생:', error)
  }
}


// 특별한 날(크리스마스, 할로윈)
const eventDay = {
  '01-01': '새해',
  '12-25': '크리스마스',
}


onMounted(() => {
  isBirthday.value = checkBirthday()
  
  if (isBirthday.value) {
    birthdayMovie()
  }
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
