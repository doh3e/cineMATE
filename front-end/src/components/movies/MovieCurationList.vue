<template>
  <div class="result-list" v-if="recommends.length > 0">
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { publicAxios } from '@/axios';

const props = defineProps({
  movie: Array,
})

</script>

<style scoped>
</style>
