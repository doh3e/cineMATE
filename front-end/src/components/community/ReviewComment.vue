<template>
  <div class="comment-container">
    <div class="comment-input">
      <form @submit.prevent="createComment">
        <label for="comment-content">
          {{ store.userInfo.nickname }}({{ store.userInfo.username }})
        </label>
        <textarea
          name="comment-content"
          id="comment-content"
          v-model="query"
          maxlength="200"
          @keyup.enter.prevent="createComment"
        ></textarea>
        <button type="submit">등록</button>
      </form>
    </div>
    <div v-if="comments.length" class="comments-listbox">
      <ReviewCommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @fetchList="fetchCommentList"
      />
    </div>
    <p v-else>댓글이 없습니다. 첫 번째 댓글을 작성해보세요!</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ReviewCommentItem from './ReviewCommentItem.vue'
import { useCounterStore } from '@/stores/counter'
import { publicAxios, authAxios } from '@/axios'

const store = useCounterStore()
const query = ref('')
const comments = ref([])

const prop = defineProps({
  review_id: {
    type: Number,
    required: true,
  },
})

// 댓글 작성 함수
const createComment = async () => {
  try {
    await authAxios.post(`/community/reviews/${prop.review_id}/comments/`, {
      content: query.value.trim(),
    })
    alert('댓글 등록이 완료되었습니다!')
    query.value = ''
    fetchCommentList()
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성 중 오류가 발생했습니다.')
  }
}

// 댓글 목록 불러오기
const fetchCommentList = async () => {
  try {
    const response = await publicAxios.get(
      `/community/reviews/${prop.review_id}/comments/`
    )
    comments.value = response.data || []
  } catch (error) {
    console.error('댓글 데이터를 가져오는 중 오류 발생:', error)
  }
}

onMounted(() => {
  fetchCommentList()
})

</script>

<style scoped>
.comment-container {
  padding: 30px 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  width: 90%;
  min-width: 400px;
  max-width: 800px;
  height: 70%;
  margin: 0 auto;
  margin-bottom: 30px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 20px;
}

.comment-input {
  width: 100%;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.comment-input > form {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

form > label {
  justify-self: flex-start;
  text-align: left;
  font-family: 'S-CoreDream';
  font-weight: 600;
}

.comments-listbox {
  width: 100%;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

#comment-content {
  width: 500px;
  resize: none;
  padding: 10px;
  font-size: 0.9rem;
}

button {
  width: 50px;
  min-width: 50px;
  height: 30px;
  cursor: pointer;
}

</style>
