<template>
  <div v-if="movies.length > 0" class="movie-slider-container">
    <Carousel v-bind="config">
      <Slide v-for="(movie, index) in movies" :key="index" class="carousel__slide">
        <MovieCurationItem :movie="movie" @open-modal="openModal" />
      </Slide>

      <!-- 네비게이션 버튼 추가 -->
      <template #addons>
        <Navigation />
      </template>
    </Carousel>
  </div>
  <div class="loading" v-else>
      <img src="@/assets/img/loading-spinner-unscreen.gif" alt="spinner" class="loading-spinner">
  </div>
  <MovieDetail
    v-if="selectedMovie && isModalVisible"
    :movie="selectedMovie"
    :isVisible="isModalVisible"
    @close="closeModal"
  />
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { Carousel, Slide, Navigation } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import MovieCurationItem from '@/components/movies/MovieCurationItem.vue'
import MovieDetail from './MovieDetail.vue'


const store = useCounterStore()

const props = defineProps({
  movies: {
    type: Array,
    default: () => []
  }
})

// 모달창 설정
const isModalVisible = ref(false)
const selectedMovie = ref(null)

// 모달 열기
const openModal = (movie) => {
  selectedMovie.value = movie
  isModalVisible.value = true
}

// 모달 닫기
const closeModal = () => {
  isModalVisible.value = false
  selectedMovie.value = null
}


// 캐러셀 설정
const config = {
  wrapAround: true,
  autoplay: 3000,
  transition: 600,
  height: 400,
  snapAlign: 'center',
  breakpoints: {
    1200: {
      itemsToShow: 5,
    },
    1000: {
      itemsToShow: 4,
    },
    700: {
      itemsToShow: 3,
    },
    450: {
      itemsToShow: 1,
    },
  },
}


</script>

<style scoped>
.carousel__slide {
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  opacity: 0.9;
  transform: scale(0.9);
  transition: transform 0.3s ease, opacity 0.3s ease;
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
  transform: scale(1);
}

.carousel__viewport {
  overflow: hidden;
  width: 100% !important;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px;
}

.carousel__track {
  display: flex;
  align-items: center;
  transform-style: preserve-3d;
}

.movie-slider-container {
  width: 100%;
  max-width: 1200px;
  min-width: 300px;
  height: 48vh;
  max-height: 450px;
  margin: 0 auto;
  padding-top: 20px;
  background-color: #f8f8f8;
  padding-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
}

</style>
