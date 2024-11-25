<template>
  <div>
    {{ review.review_title }} : {{ review.title }}
  </div>
</template>


<script setup>
const props = defineProps({
  review: Object,
})

</script>

<style scoped>
</style>
