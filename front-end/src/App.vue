<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'Home' }">Home</RouterLink>
      <RouterLink v-if="!store.userInfo" :to="{ name: 'SignUp' }">Signup</RouterLink>
      <RouterLink v-if="!store.userInfo" :to="{ name: 'Login' }">Login</RouterLink>
      <button v-else @click="handleLogout">Logout</button>
    </nav>
  </div>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from './stores/counter';

const store = useCounterStore()

const handleLogout = async () => {
  await store.logout()
  router.push({ name: 'Home' })
}


</script>

<style scoped>

</style>
