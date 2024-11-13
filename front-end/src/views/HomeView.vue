<template>
  <header class="header">
    <nav>
      <p v-if="store.userInfo">내 친구, {{ store.userInfo.username }}!</p>
      <p v-else>로그인하세요</p>
    </nav>
  </header>

  <main class="home-main">
    <h1>Top Rated Movies</h1>
    <div v-if="Array.isArray(store.top_movies) && store.top_movies.length > 0" class="movielist-box">
      <MovieListItem v-for="movie in store.top_movies" :key="movie.id" :movie="movie" />
    </div>
    <h3 v-else>영화 데이터를 불러오는 중입니다...</h3>
    <div ref="loadMoreTrigger" v-if="store.hasMore" class="loading">
      <p>Loading more movies...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useCounterStore } from '@/stores/counter';
import MovieListItem from '@/components/MovieListItem.vue';

const store = useCounterStore();
const observer = ref(null);
const loadMoreTrigger = ref(null);

onMounted(async () => {
  store.resetPagination();
  window.scrollTo(0, 0);

  try {
    await store.getUserInfo();
    console.log("유저 정보:", store.userInfo);
  } catch (error) {
    console.error("유저 정보를 불러오는 중 오류 발생:", error);
  }

  await store.loadMovies();

  observer.value = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && store.hasMore) {
      await store.loadMovies();
    }
  });

  if (loadMoreTrigger.value) {
    observer.value.observe(loadMoreTrigger.value);
  }
});

onBeforeUnmount(() => {
  if (observer.value && loadMoreTrigger.value) {
    observer.value.unobserve(loadMoreTrigger.value);
  }
});
</script>

<style scoped>
.header {
  width: 100%;
  background-color: #f8f8f8;
  padding: 1em;
  text-align: center;
  font-weight: bold;
}

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
