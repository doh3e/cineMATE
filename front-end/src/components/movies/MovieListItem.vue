<template>
  <div class="movie-item" @click="openModal">
    <img :src="store.getImageUrl(movie.poster_path)" alt="Poster" v-if="movie.poster_path" id="movie-poster">
    <h4 class="truncate">{{ movie.title }}</h4>
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
          ></i>{{ movie.likes_count }}
        </span>
      </div>
      <div class="bookmarks" @click.stop="toggleBookmark">
        <span>
          {{ movie.bookmarks_count }}
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
      movie_id: props.movie.id
    })
    const { action } = response.data
    isBookmarkAnimating.value = true
    if (action === 'added') {
      store.userInfo.bookmarked_movies.push(props.movie.id)
      props.movie.bookmarks_count++
    } else {
      const index = store.userInfo.bookmarked_movies.indexOf(props.movie.id)
      if (index !== -1) store.userInfo.bookmarked_movies.splice(index, 1)
      props.movie.bookmarks_count--
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
      movie_id: props.movie.id
    })
    const { action } = response.data
    isLikeAnimating.value = true
    if (action === 'added') {
      store.userInfo.liked_movies.push(props.movie.id)
      props.movie.likes_count++
    } else {
      const index = store.userInfo.liked_movies.indexOf(props.movie.id)
      if (index !== -1) store.userInfo.liked_movies.splice(index, 1)
      props.movie.likes_count--
    }
  } catch (error) {
    console.error('Like toggle failed:', error)
    alert('좋아요를 업데이트하는 중 문제가 발생했습니다. 다시 시도해주세요.')
  }
}


</script>

<style scoped>
.movie-item {
  flex: 1 1 250px; /* 기본 너비를 지정하고 flex-grow와 flex-shrink를 조정 */
  max-width: 250px; /* 최대 너비를 고정 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.truncate {
  display: inline-block;
  max-width: 230px; /* 제목 길이 제한 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

#movie-poster {
  width: 100%; /* 카드 너비에 맞게 설정 */
  aspect-ratio: 2 / 3; /* 이미지 비율 유지 */
  object-fit: cover; /* 비율에 맞게 잘림 */
  border-radius: 4px;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px; /* 상단과의 간격 추가 */
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
