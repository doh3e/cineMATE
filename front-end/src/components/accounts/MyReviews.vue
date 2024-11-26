<template>
  <div class="myreview-container">
    <h1 class="yesteryear-regular h1-cali">My Review State</h1>
    <div class="row-container">
      <div class="review-box written">
        <h2>내가 작성한 리뷰</h2>
        <div class="item-list"  v-if="myReviews && myReviews.length>0">
          <MyReviewItem
          v-for="review in myReviews"
          :key="review.review_id"
          :review="review"
          />
        </div>
        <div v-else>
          <h3>작성한 리뷰가 없습니다.</h3>
        </div>
      </div>


      <div class="review-box box-liked">
        <h2>내가 좋아한 리뷰</h2>
        <div class="item-list liked" v-if="likedReviews && likedReviews.length > 0">
          <MyReviewItem
          v-for="review in likedReviews"
          :key="review.review_id"
          :review="review"
          />
        </div>
        <div v-else>
          <h3>좋아한 리뷰가 없습니다.</h3>
        </div>
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

</script>

<style scoped>

.myreview-container {
  width: 100%;
  background-color: rgba(248, 248, 248, 0.8);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  gap: 30px;
  margin-bottom: 30px;
}

.row-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
}

.h1-cali {
  color: #1f1f1f;
}

.review-box {
  width: 100%;
  height: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: hidden;
  gap: 10px;
}

.review-box > h2 {
  font-family: 'S-CoreDream';
  font-weight: 600;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.item-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
  height: 300px;
  overflow-y: auto;
  background-color: #bbb;
  border-radius: 10px;
  padding: 20px;
}

.written {
  align-items: flex-start;
}

.box-liked {
  align-items: flex-end;
}

.liked {
  align-items: flex-start;
}
</style>
