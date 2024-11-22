<template>
  <div class="movie-item" @click="openModal">
    <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
    <img v-else src="@/assets/img/default_movie_poster.png" alt="Default Poster" id="movie-poster">
    <h4 class="truncate movie-title">{{ movie.title }}</h4>
    <hr class="card-line">
    <div class="action-btn">
      <div class="likes" @click.stop="toggleLike">
        <span>
          <i
            :class="{
              'fa-regular': !isLiked,
              'fa-solid': isLiked,
              'animate': isLikeAnimating
            }"
            class="fa-heart fa-lg"
            :style="{ color: isLiked ? 'red' : '#B197FC' }"
            @animationend="isLikeAnimating = false"
          ></i>
        </span>
      </div>
      <div class="bookmarks" @click.stop="toggleBookmark">
        <span>
          <i
            :class="{
              'fa-regular': !isBookmarked,
              'fa-solid': isBookmarked,
              'animate': isBookmarkAnimating
            }"
            class="fa-bookmark fa-lg"
            :style="{ color: isBookmarked ? '#7469B6' : '#B197FC' }"
            @animationend="isBookmarkAnimating = false"
          ></i>
        </span>
      </div>
    </div>
  </div>

  <MovieDetail
    v-if="movie && isModalVisible"
    :movie="movie"
    :isVisible="isModalVisible"
    @close="closeModal"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import MovieDetail from './MovieDetail.vue'
import { authAxios } from '@/axios'

const store = useCounterStore()

const props = defineProps({
  movie: Object,
})

const isModalVisible = ref(false)
const isBookmarked = computed(() => store.userInfo?.bookmarked_movies?.includes(props.movie.id))
const isLiked = computed(() => store.userInfo?.liked_movies?.includes(props.movie.id))
const isBookmarkAnimating = ref(false)
const isLikeAnimating = ref(false)

const openModal = () => {
  isModalVisible.value = true
}

const closeModal = () => {
  isModalVisible.value = false
}

const toggleBookmark = async () => {
  if (!store.userInfo || !store.userInfo.id) {
    alert('북마크 기능은 회원만 사용할 수 있습니다!')
    return
  }
  try {
    const response = await authAxios.post('/movies/bookmark/', {
      movie: props.movie
    })
    const { action } = response.data
    isBookmarkAnimating.value = true
    if (action === 'added') {
      store.userInfo.bookmarked_movies.push(props.movie.id)
    } else {
      const index = store.userInfo.bookmarked_movies.indexOf(props.movie.id)
      if (index !== -1) store.userInfo.bookmarked_movies.splice(index, 1)
    }
  } catch (error) {
    console.error('Bookmark toggle failed:', error)
    alert('북마크를 업데이트하는 중 문제가 발생했습니다. 다시 시도해주세요.')
  }
}


const toggleLike = async () => {
  if (!store.userInfo || !store.userInfo.id) {
    alert('좋아요 기능은 회원만 사용할 수 있습니다!')
    return
  }
  try {
    const response = await authAxios.post('/movies/like/', {
      movie: props.movie
    })
    const { action } = response.data
    isLikeAnimating.value = true
    if (action === 'added') {
      store.userInfo.liked_movies.push(props.movie.id)
    } else {
      const index = store.userInfo.liked_movies.indexOf(props.movie.id)
      if (index !== -1) store.userInfo.liked_movies.splice(index, 1)
    }
  } catch (error) {
    console.error('Like toggle failed:', error)
    alert('좋아요를 업데이트하는 중 문제가 발생했습니다. 다시 시도해주세요.')
  }
}
</script>

<style scoped>
.movie-item {
  flex: 1 1 250px;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0px;
  box-sizing: border-box;
  background-color: #f8f8f8;
  border-radius: 2px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  text-align: center;
  cursor: pointer;
}

.movie-title {
  width: 100%;
  padding: 10px;
}

.truncate {
  display: inline-block;
  max-width: 230px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-line {
  width: 90%;
  color: rgba(31, 31, 31, 0.3);
}

#movie-poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding: 0px 15px;
}

.likes, .bookmarks {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 5px;
}

.fa-heart, .fa-bookmark {
  cursor: pointer;
  padding: 5px;
  transition: transform 0.3s ease, color 0.3s ease;
}

.fa-heart.animate, .fa-bookmark.animate {
  animation: pop 0.3s ease;
}

@keyframes pop {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}
</style>
