<template>
  <div class="movie-container">
    <h1>영화 추천/검색 영역</h1>
    <div class="movie-head">
      <div class="tabs">
        <RouterLink
          :to="{ name: 'MovieSearch' }"
          class="tab"
          :class="{ active: $route.name === 'MovieSearch' }"
        >
          영화 검색
        </RouterLink>
        <RouterLink
          :to="{ name: 'MovieCurating' }"
          class="tab"
          :class="{ active: $route.name === 'MovieCurating' }"
        >
          큐레이팅
        </RouterLink>
      </div>

      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
const $route = useRoute()

</script>

<style scoped>
.movie-container {
  width: 80%;
  min-width: 500px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  background-color: #7469B6;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.tab.active {
  background-color: #574F9F;
}

.tab:hover {
  background-color: #574F9F;
}
</style>
