<template>
  <div class="movie-item" v-if="movie">
    <img :src="posterUrl" alt="movie poster" />
    <h4>{{ movie.title }}</h4>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
})

// 상태 저장을 위한 변수
const store = useCounterStore()

// 포스터 URL 계산
const posterUrl = computed(() => {
  if (props.movie.poster_path) {
    return store.getImageUrl(props.movie.poster_path)
  }
  // 포스터가 없을 경우 기본 이미지 경로 반환
  return new URL('@/assets/img/default_movie_poster.png', import.meta.url).href
})
</script>

<style scoped>
.movie-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background-color: #2c2c2c;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
}

.movie-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}

.movie-item img {
  width: 100%;
  max-width: 150px;
  height: auto;
  margin-bottom: 10px;
  border-radius: 4px;
}

.movie-item h4 {
  color: #f8f8f8;
  font-size: 16px;
  margin: 0;
}
</style>
