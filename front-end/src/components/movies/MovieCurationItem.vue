<template>
  <div class="movie-item" v-if="movie" @click="handleClick">
    <img :src="posterUrl" alt="Poster" v-if="movie.poster_path" id="movie-poster">
    <img v-else src="@/assets/img/default_movie_poster.png" alt="Default Poster" id="movie-poster">
    <h4 class="truncate movie-title">{{ movie.title }}</h4>
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
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { authAxios } from '@/axios'

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
})

const store = useCounterStore()
const isBookmarked = computed(() => store.userInfo?.bookmarked_movies?.includes(props.movie.id))
const isLiked = computed(() => store.userInfo?.liked_movies?.includes(props.movie.id))
const isBookmarkAnimating = ref(false)
const isLikeAnimating = ref(false)

// 포스터 URL 계산
const posterUrl = computed(() => {
  if (props.movie.poster_path) {
    return store.getImageUrl(props.movie.poster_path)
  }
  // 포스터가 없을 경우 기본 이미지 경로 반환
  return new URL('@/assets/img/default_movie_poster.png', import.meta.url).href
})


// 부모로 모달 이벤트 전달
const emit = defineEmits(['open-modal'])
const handleClick = () => {
  emit('open-modal', props.movie)
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
  flex: 1 1 200px;
  max-width: 250px;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 15px 0px;
  box-sizing: border-box;
  background-color: #1f1f1f;
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.movie-item:hover {
  cursor: pointer;

}

#movie-poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
}

.movie-title {
  width: 100%;
  padding: 8px;
  font-size: 1rem;
  color: #f8f8f8;
}

.truncate {
  display: inline-block;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  padding: 0px 10px;
}

.likes, .bookmarks {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 5px;
}

.fa-heart, .fa-bookmark {
  cursor: pointer;
  padding: 4px; /* 아이콘 패딩 축소 */
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
    transform: scale(1.2); /* 애니메이션 크기 축소 */
  }
  100% {
    transform: scale(1);
  }
}
</style>
