<template>
  <div>
    <h3>좋아하는 영화</h3>
    <ul v-if="likes && likes.length > 0">
      <li
        v-for="like in likes"
        :key="like.id"
        class="like-item"
      >
        {{ like.title }} ({{ like.release_date }})
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  likes: Object
})

</script>

<style scoped>
</style>