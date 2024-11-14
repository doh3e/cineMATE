<template>

  <div class="home-main">
    <h1>Top Rated Movies</h1>
    <div v-if="Array.isArray(store.top_movies) && store.top_movies.length > 0" class="movielist-box">
      <MovieListItem v-for="movie in store.top_movies" :key="movie.id" :movie="movie" />
    </div>
    <h3 v-else>영화 데이터를 불러오는 중입니다...</h3>
    <div ref="loadMoreTrigger" v-if="store.hasMore" class="loading">
      <p>Loading more movies...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';
import MovieListItem from '@/components/movies/MovieListItem.vue';

const store = useCounterStore();
const observer = ref(null);
const loadMoreTrigger = ref(null);

onMounted(async () => {
  store.resetPagination();
  window.scrollTo(0, 0);

  await store.loadMovies();

  observer.value = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && store.hasMore) {
      await store.loadMovies();
    }
  });

  if (loadMoreTrigger.value) {
    observer.value.observe(loadMoreTrigger.value);
  }

  await store.getUserInfo();
});

// store.userInfo를 감시하여 값이 업데이트될 때마다 반영
watch(() => store.userInfo, (newUserInfo) => {
  console.log('Updated user info:', newUserInfo);
});

onBeforeUnmount(() => {
  if (observer.value && loadMoreTrigger.value) {
    observer.value.unobserve(loadMoreTrigger.value);
  }
});
</script>

<style scoped>

.home-main {
  width: 100%;
  height: 100vh;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 50px;
}
.loading {
  text-align: center;
  padding: 1em;
}

.movielist-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
