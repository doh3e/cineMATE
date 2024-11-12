<template>
  <div>
      <nav>
        <RouterLink to="/">Home</RouterLink>
      </nav>
  </div>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<style scoped>

</style>
