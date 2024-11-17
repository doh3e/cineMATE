<template>
  <div class="myinfo-box" v-if="person">
    <h3>내 정보</h3>
    <p>{{ person?.nickname }}({{ person?.username }} )</p>
  </div>
</template>

<script setup>

const props = defineProps({
  person: Object
})

</script>

<style scoped>
</style>