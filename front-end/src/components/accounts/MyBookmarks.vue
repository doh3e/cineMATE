<template>
  <div class="bookmark-box">
    {{ bookmark.title }} ({{ bookmark.release_date }})
  </div>
</template>

<script setup>
const props = defineProps({
  bookmark: Object
})

</script>

<style scoped>
</style>
