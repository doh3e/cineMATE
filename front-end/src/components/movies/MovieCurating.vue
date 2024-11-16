<template>
  <div>
    <button @click="recommendMovies">추천받기</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { publicAxios } from '@/axios';

const recommendMovies = async () => {
  try {
    const response = await publicAxios.get('/movies/recommend/')
    const movies = response.data.results
    const hasMore = response.data.next !== null

    // 추천 결과를 부모로 전달
    emit('recommend', { movies, hasMore })
  } catch (error) {
    console.error('추천 중 오류 발생:', error)
  }
}

const emit = defineEmits(['recommend']) // 추천 이벤트 정의
</script>

<style scoped>
</style>
