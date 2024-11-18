<template>
  <div>
    <h2>저장소</h2>
      <div class="like-movies">
        <h3>좋아하는 영화</h3>
        <MyLikes
        v-for="like in likes"
        :key="like.id"
        :like="like"
        />
      </div>
      <div class="bookmark-movies">
        <h3>보고싶은 영화</h3>
        <MyBookmarks
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        :bookmark="bookmark"
        />
      </div>
  </div>
</template>

<script setup>
import MyLikes from './MyLikes.vue';
import MyBookmarks from './MyBookmarks.vue';

const props = defineProps({
  bookmarks: Array,
  likes: Array,
})

</script>

<style scoped>
</style>