<template>
  <div class="bookmark-box">
    <h3>보고싶은 영화</h3>
    <ul v-if="bookmarks && bookmarks.length > 0">
      <li
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        class="bookmark-item"
      >
        {{ bookmark.title }} ({{ bookmark.release_date }})
      </li>
    </ul>
  </div>
</template>

<script setup>

const props = defineProps({
  bookmarks: Object
})

</script>

<style scoped>
</style>
