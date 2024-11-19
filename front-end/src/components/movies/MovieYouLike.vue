<template>
  <div class="result-list" v-if="recommends.length > 0">
    <h3>{{ store.userInfo.nickname }} 님이 선호할만한 장르의 영화</h3>
    <MovieList
        :movies="recommends"
      />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { publicAxios } from '@/axios';
import { useCounterStore } from '@/stores/counter';
import MovieList from './MovieList.vue';

const store = useCounterStore()
const props = defineProps({
  recommends: Array,
})

</script>

<style scoped>
.result-list {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>
