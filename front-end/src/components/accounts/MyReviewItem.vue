<template>
  <div class="review-item" @click="goReviewDetail(review.review_id)">

    <h3>❝ <span>{{ review.review_title }}</span> ❞</h3>
    <p>{{ review.title }} ({{ review.release_date.slice(0,4) }})</p>

  </div>
</template>


<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  review: Object,
})

const goReviewDetail = (review_id) => {
  router.push({name: 'ReviewDetail', params: {review_id: review_id}})
}

</script>

<style scoped>

.review-item {
  flex: 0 1 calc(50% - 20px);
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  background-color: #f8f8f8;
  padding: 10px 20px;
  border-radius: 20px;
  box-shadow: 2px 2px 2px #1f1f1f;
  overflow: hidden;
  transition: all 0.3s ease;
}

.review-item > h3 {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 1.3rem;
}

.review-item:hover {
  transform: scale(1.05);
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.3);
  background-color: rgba(173, 136, 198, 0.5);
  cursor: pointer;
}

@media screen and (max-width: 1056px) {
  .review-item {
    flex: 0 1 100%;
    height: 100px;
  }
}
</style>
