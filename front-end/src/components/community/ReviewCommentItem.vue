<template>
  <div class="comment-item">
    <div class="user-name">
      <span>{{ comment?.user.nickname }}</span>
    </div>
    <div class="comment-content">
      <span>{{ comment?.content }}</span>
    </div>
    <div class="create-time">
      <span>{{ formatDate(comment?.created_at) }}</span>
    </div>
    <div class="delete-btn" v-if="isMyComment">
      <i class="fa-solid fa-x fa-2xs" style="color: #c8c4d4;" @click="deleteComment"></i>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { publicAxios, authAxios } from '@/axios'

const prop = defineProps({
  comment: Object,
})
const store = useCounterStore()
const isMyComment = computed(() => {
  return store.userInfo?.id === prop.comment.user.id
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
}

const emit = defineEmits(['fetchList'])

const deleteComment = async () => {
  if(!isMyComment) {
    alert('이 댓글을 삭제할 권한이 없습니다.')
    return
  }

  const isConfirmed = confirm('정말 이 댓글을 삭제하시겠어요?')
  if(!isConfirmed) {
    return
  }

  try {
    await authAxios.delete(`/community/reviews/${prop.comment?.review}/comments/${prop.comment?.id}/`)
    alert('댓글이 삭제되었습니다!')
    emit('fetchList')
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제 중 오류가 발생했습니다.')
  }
}

</script>


<style scoped>

.comment-item {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  padding: 10px 20px;
  font-size: 0.9rem;
  border-radius: 5px;
  box-shadow: 1px 1px 1px gray;
}

.user-name {
  width: 15%;
  justify-self: flex-start;
  text-align: left;
  font-weight: 600;
}

.comment-content {
  width: 65%;
  justify-self: flex-start;
  text-align: left;
}

.create-time {
  justify-self: flex-end;
  text-align: right;
  font-size: 0.8rem;
}

.delete-btn {
  width: 3%;
  justify-self: flex-end;
  text-align: right;
}

</style>