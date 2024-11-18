<template>
  <div>
    {{ review.review_title }} : {{ review.title }}
  </div>
</template>


<script setup>
const props = defineProps({
  review: Object,
})

console.log(props.review)
</script>

<style scoped>
</style>
