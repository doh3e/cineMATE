<template>
  <div>

    {{ like.title }} ({{ like.release_date }})
  
  </div>
</template>

<script setup>
const props = defineProps({
  like: Object
})

</script>

<style scoped>
</style>