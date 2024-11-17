<template>
  <div class="review-box">
    <h2>리뷰 게시판</h2>
    <table>
      <thead>
        <tr>
          <th id="index-num">번호</th>
          <th id="rv-title">리뷰 제목</th>
          <th id="mv-title">영화 제목</th>
          <th id="writer">작성자</th>
          <th id="date">작성일</th>
          <th id="like">추천</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(review) in reviews"
          :key="review.review_id"
          @click="goToDetail(review.review_id)"
          style="cursor: pointer"
        >
          <td class="index-num-data">{{ review.review_id }}</td>
          <td>{{ review.review_title }} <span class="comment-cnt">[{{review.comment_count}}]</span></td>
          <td>{{ review.title }}</td>
          <td class="writer-data">{{ review.user.nickname || review.user.username }}</td>
          <td class="date-data">{{ formatDate(review.created_at) }}</td>
          <td class="like-data">{{ review.like_count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
      >
        ◀
      </button>
      <button
        v-for="page in totalPages"
        :key="page"
        @click="changePage(page)"
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
      <button
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
      >
        ▶
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onBeforeRouteUpdate } from 'vue-router'
import { publicAxios } from '@/axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToDetail = (reviewId) => {
  router.push({ name: 'ReviewDetail', params: { review_id: reviewId } })
}

// 상태 변수
const reviews = ref([]) // 리뷰 데이터
const currentPage = ref(1) // 현재 페이지
const totalPages = ref(1) // 총 페이지 수
const pageSize = 5 // 한 페이지에 표시할 리뷰 수

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false, // 24시간 형식 사용
  })
}

// 리뷰 데이터 가져오기
const fetchReviews = async (page = 1) => {
  try {
    const response = await publicAxios.get('/community/reviews/', { params: { page } })
    reviews.value = response.data.results
    currentPage.value = response.data.current_page
    totalPages.value = response.data.total_pages
  } catch (error) {
    console.error('리뷰 데이터를 가져오는 중 오류 발생:', error)
  }
}

// 페이지 변경
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  fetchReviews(page)
}

// 최초 데이터 로드
onMounted(() => {
  fetchReviews()
})

// 라우트 변경 시 데이터 갱신
onBeforeRouteUpdate((to, from, next) => {
  if (to.name === 'ReviewList') {
    fetchReviews()
  }
  next()
})

</script>

<style scoped>
.review-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

table {
  width: 90%;
  border-collapse: collapse;
  margin: 20px 0;
  min-width: 400px;
}
thead th {
  background-color: #f4f4f4;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
}
tbody td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

#index-num {
  width: 5%;
  text-align: center;
}

#rv-title {
  width: 35%;
  text-align: center;
}

#mv-title {
  width: 20%;
  text-align: center;
}

#writer{
  width: 15%;
  text-align: center;
}

#date {
  width: 20%;
}

#like {
  width: 10%;
  text-align: center;
}

.index-num-data,
.writer-data,
.like-data {
  text-align: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
}
.pagination button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
