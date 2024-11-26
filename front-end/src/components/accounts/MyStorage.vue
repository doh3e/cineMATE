<template>
  <div>
    <!-- 좋아하는 영화 캐러셀 -->
    <div class="carousel-container like-movies">
      <h3 class="yesteryear-regular">Beloved,</h3>
      <Carousel
        :wrapAround="true"
        :height="300"
        :transition="0.5"
        :itemsToShow="5"
        :responsive="responsiveBreakpoints"
        loop
        mouse-drag
        touch-drag
      >

        <template #prev>
          <button class="prev-btn">◀</button>
        </template>
        <template #next>
          <button class="next-btn">▶</button>
        </template>

        <template v-for="like in likes" :key="like.id">
          <Slide>
            <MyStorageItem :movie="like" @showDetail="openModal"/>
          </Slide>
        </template>
      </Carousel>
    </div>

    <!-- 보고 싶은 영화 캐러셀 -->
    <div class="carousel-container bookmark-movies">
      <h3 class="yesteryear-regular">Bookmarked,</h3>
      <Carousel
        :wrapAround="true"
        :height="300"
        :transition="0.5"
        :itemsToShow="5"
        :responsive="responsiveBreakpoints"
        loop
        mouse-drag
        touch-drag
      >

        <template #prev>
          <button class="prev-btn">◀</button>
        </template>
        <template #next>
          <button class="next-btn">▶</button>
        </template>

        <template v-for="bookmark in bookmarks" :key="bookmark.id">
          <Slide>
            <MyStorageItem :movie="bookmark" @showDetail="openModal"/>
          </Slide>
        </template>
      </Carousel>
    </div>
    <!-- 모달 컴포넌트 -->
    <MovieDetail
      v-if="isModalVisible"
      :movie="selectedMovie"
      :isVisible="isModalVisible"
      @close="closeModal"
    />

  </div>
</template>

<script setup>
import { Carousel, Slide } from 'vue3-carousel';
import { ref } from 'vue';
import 'vue3-carousel/dist/carousel.css';
import MyStorageItem from './MyStorageItem.vue';
import MovieDetail from '../movies/MovieDetail.vue';

const props = defineProps({
  bookmarks: Array,
  likes: Array,
});

const isModalVisible = ref(false);
const selectedMovie = ref(null);

const openModal = (movie) => {
  selectedMovie.value = movie;
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
  selectedMovie.value = null;
};

const responsiveBreakpoints = [
  {
    breakpoint: 1000, // 화면이 1200px 이하일 때
    settings: {
      itemsToShow: 4,
      itemsToScroll: 1,
    },
  },
  {
    breakpoint: 800, // 화면이 800px 이하일 때
    settings: {
      itemsToShow: 3,
      itemsToScroll: 1,
    },
  },
  {
    breakpoint: 600, // 화면이 600px 이하일 때
    settings: {
      itemsToShow: 2,
      itemsToScroll: 1,
    },
  },
  {
    breakpoint: 400, // 화면이 400px 이하일 때
    settings: {
      itemsToShow: 1,
      itemsToScroll: 1,
    },
  },
];
</script>

<style scoped>
.carousel-container {
  margin: 0 auto; /* 가운데 정렬 */
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: rgba(248, 248, 248, 0.8);
  overflow: hidden;
  position: relative;
  max-width: 1200px; /* 최대 너비 */
  width: 90%; /* 전체 부모 요소의 90%로 설정 */
  min-width: 250px; /* 최소 너비 */
  height: 350px;
  box-sizing: border-box; /* 패딩 포함 */
}

.carousel-container h3 {
  width: 100%;
  text-align: center;
  font-size: 2rem;
}

.carousel-container .movie-item img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.prev-btn,
.next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.7); /* 반투명 배경 */
  color: white;
  border: none;
  padding: 15px 20px;
  font-size: 1.5rem; /* 버튼 글자 크기 */
  cursor: pointer;
  z-index: 10;
  border-radius: 50%; /* 동그랗게 */
  transition: background 0.3s ease;
}

.prev-btn {
  left: -20px; /* 왼쪽 위치 */
}

.next-btn {
  right: -20px; /* 오른쪽 위치 */
}

.carousel__viewport {
  display: flex;
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: center; /* 필요 시 가로 중앙 정렬 */
  height: 100%; /* 뷰포트 높이를 100%로 설정 */
}

.prev-btn:hover,
.next-btn:hover {
  background: rgba(0, 0, 0, 0.9); /* hover 시 배경 어둡게 */
}

.carousel__slide {
  width: 220px !important; /* 슬라이드 너비 고정 */
  height: 220px !important; /* 슬라이드 높이 고정 */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  margin: auto; /* 슬라이드가 부모 안에서 중앙 정렬 */
}
</style>
