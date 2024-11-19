<template>
  <div class="curation-title">
    <h3>🎉 생일 축하해요, {{ store.userInfo.nickname }}님! 🎉</h3>
    <p> 당신이 태어난 해에 개봉한 영화들을 보여줄게요. </p>
  </div>
  <div v-if="movies.length > 0" class="movie-slider-container">
    <Carousel v-bind="config">
      <Slide v-for="(movie, index) in movies" :key="index" class="carousel__slide">
        <MovieCurationItem :movie="movie" />
      </Slide>

      <!-- 네비게이션 버튼 추가 -->
      <template #addons>
        <Navigation />
      </template>
    </Carousel>
  </div>
  <div v-else class="loading-container">
    <p>Loading movies...</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { Carousel, Slide, Navigation } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import MovieCurationItem from '@/components/movies/MovieCurationItem.vue'


const store = useCounterStore()

const props = defineProps({
  movies: {
    type: Array,
    default: () => []
  }
})

// 캐러셀 설정
const config = {
  itemsToShow: 3.95, // 자연스러운 4개 표시
  wrapAround: true,  // 무한 루프
  autoplay: 3000,    // 3초마다 자동 슬라이드
  transition: 500,   // 부드러운 전환
}
</script>

<style scoped>
.carousel__slide {
  padding: 5px;
}

.carousel__viewport {
  perspective: 2000px;
}

.carousel__track {
  transform-style: preserve-3d;
}

.carousel__slide {
  opacity: 0.9;
  transform: rotateY(-20deg) scale(0.9);
}

.carousel__slide--active ~ .carousel__slide {
  transform: rotateY(20deg) scale(0.9);
}

.carousel__slide--prev {
  opacity: 1;
  transform: rotateY(-10deg) scale(0.95);
}

.carousel__slide.carousel__slide--next {
  opacity: 1;
  transform: rotateY(10deg) scale(0.95);
}

.carousel__slide--active {
  opacity: 1;
  transform: rotateY(0) scale(1);
}

/* 슬라이더 컨테이너 */
.movie-slider-container {
  position: relative;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px 0;
  background-color: #1f1f1f;
  border-radius: 12px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  background-color: #f0f0f0;
  font-size: 18px;
  color: #999;
}
</style>
