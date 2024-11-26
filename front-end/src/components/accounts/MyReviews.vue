<template>
  <div class="myreview-container">
    <h1>나의 리뷰</h1>
    <div v-if="myReviews">
      <h3>내가 작성한 리뷰</h3>
      <MyReviewItem
      v-if="myReviews.length>0"
      v-for="review in myReviews"
      :key="review.review_id"
      :review="review"
      />
      <div v-else>
        <p>작성한 리뷰가 없습니다.</p>
      </div>
    </div>


    <div v-if="likedReviews">
      <h3>내가 좋아한 리뷰</h3>
      <MyReviewItem
      v-if="likedReviews.length>0"
      v-for="review in likedReviews"
      :key="review.review_id"
      :review="review"
      />
      <div v-else>
        <p>좋아한 리뷰가 없습니다.</p>
      </div>
    </div>
  </div>
</template>


<script setup>
import MyReviewItem from './MyReviewItem.vue';
const props = defineProps({
  likedReviews: Array,
  myReviews: Array,
})

console.log(props.likedReviews)
console.log(props.myReviews)
</script>

<style scoped>

.myreview-container {
  width: 100%;
  background-color: #f8f8f8;
}

</style>
