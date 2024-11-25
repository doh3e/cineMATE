<template>
  <div class="test-container">
    <!-- 이름 입력 단계 -->
    <div class="test-box" v-if="currentStep === -1">
      <div class="testimg start-img">
        <img src="@/assets/img/mvforyou-logo.png" alt="test-logo" class="test-logo">
        <h2 class="qname">{{ typedText }}<span v-if="showCaret" class="caret">_</span></h2>
        <input v-model="friendName" type="text" placeholder="이름/별명 5글자까지"
        maxlength="5"
        @keyup.enter="startTest" />
        <img src="@/assets/img/mvforyou-start-cat.png" alt="test-cat" class="test-cat">
        <button class="start-btn" @click="startTest">다음으로 →</button>
      </div>
      <div class="backgroundimg start-bg">
        <img :src="DefaultbackgroundImage" alt="test-background">
      </div>
    </div>

    <!-- 질문 단계 -->
    <div class="test-box" v-else-if="currentStep >= 0 && currentStep < questions.length">
      <div class="testimg qna">
        <h2 class="question">
          {{ currentQuestion.title.replace('[ ]', friendName) }}
        </h2>
        <div class="choices">
          <button
            class="choice-btns"
            v-for="(choice, index) in currentQuestion.choices"
            :key="index"
            @click="handleChoice(choice, index)"
          >
            ▶ {{ choice.text }}
          </button>
        </div>
      </div>
      <div class="backgroundimg questionbg">
        <img v-if="currentBackground" :src="currentBackground" alt="질문 이미지" class="question-image" />
      </div>
    </div>

    <!-- 9번 질문 -->
    <div class="test-box" v-else-if="currentStep === questions.length">
      <div class="testimg qna">
        <h2 class="question">{{ `9. ${friendName || '그 사람'} 이/가 태어난 달이 언제인지 알고있어? 만약 모른다면 어울리는 달을 골라줘!` }}</h2>
        <select v-model="birthMonth" class="month-select">
          <option value="" disabled>월을 선택하세요</option>
          <option v-for="month in 12" :key="month" :value="month">
            {{ month < 10 ? '0' + month : month }} 월
          </option>
        </select>
        <button class="start-btn" :disabled="!birthMonth" @click="nextStep">다음</button>
      </div>
      <div class="backgroundimg start-bg">
        <img src="@/assets/img/question-month.png" alt="test-9">
      </div>
    </div>

    <!-- 10번 질문 -->
    <div class="test-box" v-else-if="currentStep === questions.length + 1">
      <div class="testimg qna">
        <h2 class="question">{{ `10. 마지막으로, ${friendName} 에게 하고 싶은 말이 있어?` }}</h2>
        <textarea
          v-model="finalMessage"
          maxlength="50"
          placeholder="최대 50자까지 입력 가능"
        ></textarea>
        <button class="start-btn" :disabled="!finalMessage" @click="submitResults">결과 보기</button>
      </div>
      <div class="backgroundimg start-bg">
        <img :src="DefaultQuestionImage" alt="test-background">
      </div>
    </div>

    <!-- 결과 화면 -->
    <div class="test-box" v-else-if="resultData && currentStep === questions.length + 2">
      <div class="result-container" v-if="resultData && resultData.movie">
        <div class="result-items">
          <h1 class="friend-name">{{ resultData?.my_choice.friend_name }}</h1>
          <h1 class="friend-title">{{ resultData?.movie.title }} ({{ resultData?.movie.release_date.slice(0,4) }})</h1>
          <div class="movie-rating">
            <span v-for="n in fullStars" :key="'full-' + n">
              <img src="@/assets/img/full-star.png" alt="Full Star" class="star" />
            </span>
            <span v-if="hasHalfStar">
              <img src="@/assets/img/half-star.png" alt="Half Star" class="star" />
            </span>
            <span v-for="n in emptyStars" :key="'empty-' + n">
              <img src="@/assets/img/empty-star.png" alt="Empty Star" class="star" />
            </span>
          </div>
          <div class="desc-box">
            <p> <span>{{ resultData?.my_choice.top_genre }}</span> 장르를 좋아하는 당신은
              <span>{{ resultData?.my_choice.preference }}</span> 취향의 소유자!
            </p>
          </div>
          <div class="message-box">
            <p>{{ resultData?.my_choice.final_message }}</p>
            <img src="@/assets/img/speech-bubble.png" alt="talkbox">
          </div>
          <img src="@/assets/img/pigtail.png" alt="pigtail" class="pigtail">
          <h2 class="friend-state">{{chosenMind}}!!</h2>
          <img src="@/assets/img/mvforyou-start-cat.png" alt="result-cat" class="result-cat" v-if="chosenMind === '새가슴'">
          <img src="@/assets/img/mvforyou-blackcat.png" alt="result-cat" class="result-cat" v-if="chosenMind === '강심장'">
        </div>
        <div class="backgroundimg result-bg">
          <img src="@/assets/img/test-result.png" alt="result-background">
        </div>
        <div class="movie-poster-bg">
          <img :src="resultData?.movie.poster_base64 || '@/assets/img/default_movie_poster.png'" alt="poster">
        </div>
      </div>

      <!-- 버튼들 -->
      <div class="buttons">
        <button @click="saveScreenshot">결정 및 저장</button>
        <button @click="retryTest">다시하기</button>
        <button @click="shareResult">공유하기</button>
      </div>
    </div>

    <!-- 로딩 화면 -->
    <div class ="loading-status" v-else-if="isLoading">
      <h2 class="load-message">결과를 불러오는 중...</h2>
      <img src="@/assets/img/loading-spinner-unscreen.gif" alt="spinner" class="loading-spinner">
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import html2canvas from 'html2canvas'
import { publicAxios, authAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter'
import DefaultbackgroundImage from '@/assets/img/mvforyou-start-bg.png'
import DefaultQuestionImage from '@/assets/img/question1.png'
import QuestionZombieImage from '@/assets/img/question-zombie.png'

const store = useCounterStore()

const emit = defineEmits(['close', 'testComplete'])
const friendName = ref('') // 입력한 친구 이름/별명
const birthMonth = ref('') // 선택한 태어난 달
const finalMessage = ref('') // 입력한 메시지
const currentStep = ref(-1) // -1: 이름 입력, 0 이상: 질문 단계
const chosenPreference = ref('') // 취향설정
const chosenMind = ref('') // 강심장새가슴
const resultData = ref(null)
const isLoading = ref(false) // 로딩 상태

const closeTest = () => {
  resetState()
  emit('close') // 부모 컴포넌트로 이벤트 전달
}

// 질문 데이터
const questions = [
  {
    title: '1. [ ]의 첫인상은 어땠어?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '말수가 적고 조용했어', genres: { 드라마: 3, 가족: 3, 다큐멘터리: 2, 미스터리: 2, 스릴러: 1, 범죄: 1, 로맨스: 1 } },
      { text: '활기차고 에너지가 넘쳤어', genres: { 액션: 3, 코미디: 3, 모험: 2, 판타지: 2, 음악: 1, 로맨스: 1 } },
      { text: '어딘가 신비롭고 낭만적이었어', genres: { 미스터리: 3, 로맨스: 3, 판타지: 2, SF: 2, 음악: 2, 드라마: 1 } },
      { text: '차갑고 도도한 분위기였어', genres: { 범죄: 3, 스릴러: 3, 공포: 3, 미스터리: 2, 다큐멘터리: 2, SF: 1 } }
    ]
  },
  {
    title: '2. [ ] (이)랑 대화할 땐 어떤 느낌이 들어?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '자기 이야기를 잘 안 해줘', genres: { 미스터리: 3, 드라마: 3, 공포: 2, 범죄: 2, 다큐멘터리: 1, 가족: 1 } },
      { text: '내 고민이나 힘든 점을 잘 해결해줘', genres: { 다큐멘터리: 3, 스릴러: 2, 가족: 2, 모험: 1, 미스터리: 1 } },
      { text: '나의 말에 잘 귀 기울이고 공감해줘', genres: { 드라마: 3, 가족: 3, 음악: 2, 로맨스: 2, 코미디: 1, SF: 1, 판타지: 1 } },
      { text: '재미있는 얘기가 끊이질 않아', genres: { 코미디: 3, 액션: 3, 모험: 2, 판타지: 2, 음악: 2, 공포: 1, 범죄: 1 } }
    ],
  },
  {
    title: '3. [ ] 은/는 어떤 취향을 가지고 있는 것 같아?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '사람들이 좋아하는 건 다 좋아해!', genres: { 드라마: 2, 로맨스: 2, 가족: 2, 액션: 2, 코미디: 2, 모험: 2, 음악: 2 }, preference: '좋은게좋은' },
      { text: '남들이 좋아하는 걸 따라가는 건 별로야.', genres: { 미스터리: 2, 스릴러: 2, 범죄: 2, 다큐멘터리: 2, 공포: 2, SF: 2, 판타지: 2 }, preference: '홍대병' },
      { text: '적당히 대중적이면서도 적당히 자기 취향이 있는 것 같아.', genres: { 드라마: 2, 로맨스: 2, 코미디: 2, 모험: 2, 판타지: 2, SF: 2, 스릴러: 2, 미스터리: 2 }, preference: '평범'}
    ]
  },
  {
    title: '4. “영화 <부산행>처럼 어느 날 좀비가 생겨서 대피해야한다면 어떨 것 같아?” 라고 물어보자 [ ] 은/는…',
    backgroundImage: QuestionZombieImage,
    choices: [
      { text: '헉 어떻게 해! 사실 예전부터 생각해보긴 했어. 먹을 건 이렇게 준비를 하고, 대피는 저렇게….', genres: { 판타지: 3, 모험: 3, SF: 3, 드라마: 2, 공포: 2, 스릴러: 2, 코미디: 1, 액션: 1, 음악: 1 } },
      { text: '근데 좀비는 어떻게 걸어다니는 거지? 어떤 매커니즘인지 궁금한데?', genres: { SF: 3, 판타지: 3, 다큐멘터리: 2, 범죄: 2, 미스터리: 2, 모험: 1, 스릴러: 1 } },
      { text: '또 이상한 생각하네. 그런 일이 있을리가 없잖아!', genres: { 다큐멘터리: 3, 로맨스: 3, 범죄: 2, 스릴러: 2, 드라마: 1 } }
    ]
  },
  {
    title: '5. [ ] 은/는 강심장이야? 아니면 새가슴이야?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '강심장!', genres: { 공포: 3, 스릴러: 3, 액션: 3, 범죄: 2, 미스터리: 2, 모험: 1 }, mind: '강심장' },
      { text: '새가슴!', genres: { 드라마: 3, 가족: 3, 로맨스: 2, 음악: 2, 다큐멘터리: 2, 판타지: 1, SF: 1 }, mind: '새가슴' },
    ]
  },
  {
    title: '6. [ ] 은/는 영화를 볼 때 주로 혼자 봐, 아니면 다른 사람과 같이 봐?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '혼자!', genres: { 다큐멘터리: 3, 스릴러: 3, 범죄: 3, 공포: 2, 미스터리: 2, 판타지: 1, 드라마: 1, } },
      { text: '같이!', genres: { 가족: 3, 코미디: 3, 액션: 3, 모험: 2, 로맨스: 2, 드라마: 2, 음악: 1, 공포: 1 } },
    ]
  },
  {
    title: '7. [ ]에게 “영화속 주인공이 된다면 어떤 스토리의 영화에 출연하고 싶어?” 라고 물어보면',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '끝없는 모험과 위험이 가득한 스토리', genres: { 모험: 3, SF: 3, 판타지: 3, 액션: 2, 코미디: 2, 범죄: 1, 공포: 1, } },
      { text: '따뜻하고 감동적인 서사가 있는 스토리', genres: { 가족: 3, 드라마: 3, 로맨스: 2, 음악: 2, 다큐멘터리: 2, 코미디: 1, SF: 1, 판타지: 1 } },
      { text: '생각지도 못한 반전과 긴장감 넘치는 스토리', genres: { 미스터리: 3, 스릴러: 3, 범죄: 2, 공포: 2, 다큐멘터리: 1, 드라마: 1 } },
      { text: '사랑과 우정이 넘치는 낭만적인 스토리', genres: { 로맨스: 3, 음악: 3, 판타지: 2, 모험: 2, 가족: 2, 코미디: 1, 드라마: 1 } },
    ]
  },
  {
    title: '8. [ ] 은/는 스트레스를 받을 때 어떻게 푸는 것 같아?',
    backgroundImage: DefaultQuestionImage,
    choices: [
      { text: '혼자만의 시간을 보내며 풀더라!', genres: { 다큐멘터리: 3, 드라마: 3, 미스터리: 2, 공포: 2, 스릴러: 2, 판타지: 1, SF: 1 } },
      { text: '사람들하고 이야기하면서 풀더라!', genres: { 코미디: 3, 가족: 3, 음악: 3, 로맨스: 2, 모험: 2, 액션: 2, 드라마: 1 } },
      { text: '새로운 도전을 하거나 취미에 몰입하더라!', genres: { 모험: 3, 액션: 3, SF: 3, 판타지: 2, 스릴러: 2, 미스터리: 2, 코미디: 1, 드라마: 1 } },
      { text: '재밌는 영상이나 콘텐츠를 보며 잊더라!', genres: { 코미디: 3, 가족: 3, 액션: 3, 로맨스: 2, 음악: 2, 판타지: 1 } },
    ]
  },
]

// 현재 질문
const currentQuestion = computed(() => {
  if (currentStep.value < 0 || currentStep.value >= questions.length) return null
  const question = questions[currentStep.value]
  return {
    ...question,
    title: question.title.replace('[ ]', friendName.value || '그 사람')
  }
})

// 현재 배경화면
const currentBackground = computed(() => {
  if (currentStep.value >= 0 && currentStep.value < questions.length) {
    return questions[currentStep.value].backgroundImage;
  }
  return DefaultQuestionImage;
});


const isTestComplete = computed(() => currentStep.value >= questions.length - 1)
const genreScores = ref({})

const startTest = () => {
  currentStep.value = 0
}

const handleChoice = (choice) => {
  for (const genre in choice.genres) {
    if (!genreScores.value[genre]) genreScores.value[genre] = 0
    genreScores.value[genre] += choice.genres[genre]
  }
  if (currentStep.value === 2 && choice.preference) {
    chosenPreference.value = choice.preference
  }
  if (currentStep.value === 4 && choice.mind) {
    chosenMind.value = choice.mind;
  }
  nextStep()
}

const nextStep = () => {
  currentStep.value++
}

const submitResults = async () => {
  const topGenre = Object.keys(genreScores.value).reduce((a, b) =>
    genreScores.value[a] > genreScores.value[b] ? a : b
  )

  const result = {
    friendName: friendName.value,
    topGenre,
    birthMonth: birthMonth.value,
    finalMessage: finalMessage.value,
    preference: chosenPreference.value
  }

  isLoading.value = true
  currentStep.value = questions.length + 2

  try {
    const response = await authAxios.get('/community/test-result/', {params:result})
    resultData.value = response.data
  } catch (error) {
    console.error('결과 전송 실패:', error)
  } finally {
    isLoading.value = false // 로딩 종료
  }
}

// 평점 별로 치환하는 로직
const maxStars = 5
const roundedRating = computed(() => Math.round(resultData?.value.movie.vote_average) / 2)
const fullStars = computed(() => Math.floor(roundedRating.value))
const hasHalfStar = computed(() => roundedRating.value % 1 !== 0)
const emptyStars = computed(() => maxStars - fullStars.value - (hasHalfStar.value ? 1 : 0))

const retryTest = () => {
  resultData.value = null
  currentStep.value = -1
  friendName.value = ''
  birthMonth.value = ''
  finalMessage.value = ''
  genreScores.value = {}
  chosenPreference.value = ''
  chosenMind.value = ''
  isLoading.value = false

  // 화면을 다시 렌더링하도록 추가 처리
  console.log('테스트가 초기화되었습니다.')
  alert('처음으로 돌아갑니다!')
}

const shareResult = () => {
  alert('공유 기능이 준비 중입니다!')
}

watch(
  resultData,
  (newVal, oldVal) => {
    if (newVal) {
      console.log('결과가 도착했습니다:', newVal)
    }
  }
)

watch(
  isLoading,
  (newVal) => {
    if (newVal) {
      console.log('결과를 불러오는 중...')
    } else {
      console.log('결과 로딩 완료')
    }
  }
)

// 결과 이미지 저장 로직
const saveScreenshot = async () => {
  const resultContainer = document.querySelector('.result-container')

  if (resultContainer) {
    try {
      const canvas = await html2canvas(resultContainer, {
        useCORS: true,
        crossOrigin: "anonymous",
        scale: 1, // 캡처의 해상도
      })
      const image = canvas.toDataURL('image/png')

      // 이미지 다운로드
      const link = document.createElement('a')
      link.href = image
      link.download = `cinemate_movieforyou_${store.userInfo.username}.png`
      link.click()

      // 이미지와 데이터를 서버로 전송
      await uploadResult(image)

      alert('결과가 저장되었습니다!')
    } catch (error) {
      console.error('이미지 저장 실패:', error)
      alert('이미지 저장 중 문제가 발생했습니다.')
    }
  } else {
    alert('결과 컨테이너를 찾을 수 없습니다.')
  }
}

const uploadResult = async (image) => {
  const formData = new FormData()
  formData.append('friend_name', resultData.value?.my_choice.friend_name)
  formData.append('movie_id', resultData.value?.movie.id)
  formData.append('movie_title', resultData.value?.movie.title)
  formData.append('overview', resultData.value?.movie.overview)
  formData.append('adult', resultData.value?.movie.adult)
  formData.append('popularity', resultData.value?.movie.popularity)
  formData.append('vote_average', resultData.value?.movie.vote_average)
  formData.append('release_date', resultData.value?.movie.release_date)
  formData.append('genre_ids', JSON.stringify(resultData.value?.movie.genre_ids))
  formData.append('poster_path', resultData.value?.movie.poster_path || '')
  formData.append('card_img', image)

  try {
    const response = await authAxios.post('/community/save-result/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    console.log('업로드 성공:', response.data)
    alert('결과가 서버에 저장되었습니다!')
  } catch (error) {
    console.error('업로드 실패:', error)
    alert('서버에 저장하는 중 문제가 발생했습니다.')
  }
}




// 시작 화면 텍스트 효과
const text = "영화의 주인공은…▼"
const typedText = ref('')
const showCaret = ref(true)

let index = 0

function typeText() {
  if (index < text.length) {
    typedText.value += text[index]
    index++
    setTimeout(typeText, 100)
  }
}

// 커서 깜박임 효과
function toggleCaret() {
  showCaret.value = !showCaret.value
}

onMounted(() => {
  typeText()
  setInterval(toggleCaret, 500)
})

</script>

<style scoped>

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}


.test-container {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
}

.test-box{
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.start-bg {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.start-bg > img {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  position: relative;
}

.testimg {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  position: absolute;
  z-index: 20000;
  overflow: hidden;
  text-align: center;
}

.test-logo {
  position: absolute;
  width: 100%;
  top: 50px;
  left: 0;
  animation: float 2s ease infinite;
}

.qname {
  z-index: 21000;
  width: 80%;
  font-family: 'DungGeunMo';
  font-size: 1.5rem;
  text-align: left;
  word-wrap: break-word;
  position: absolute;
  top:400px;
  left: 25%;
  font-family: 'DungGeunMo';
  font-size: 2rem;
  white-space: nowrap;
  overflow: hidden;
}

.start-img > input[type=text] {
  position: absolute;
  top: 450px;
  left: 33%;
  width: 200px;
  height: 50px;
  padding: 10px 15px;
  text-align: center;
  font-family: 'DungGeunMo';
  font-size: 1.3rem;
}

.test-cat {
  position: absolute;
  width: 400px;
  top: 500px;
  left: 45%;
  animation: float 3s ease-in-out infinite;
}

.start-btn {
  position: absolute;
  width: 200px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  top: 670px;
  left: 33%;
  font-family: 'DungGeunMo';
  font-size: 1.5rem;
  border: 2px solid #1f1f1f;
  border-radius: 3px;
  background-color: #AD88C6;
  box-shadow: 2px 2px solid black;
}

.start-btn:hover {
  background-color: #7469B6;
  cursor: pointer;
}

.qna {
  position: absolute;
  gap:30px;
  z-index: 20000;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 200px;
  align-items: center;
}

.questionbg {
  width: 100%;
  height: 100%;
  position: relative;
}

.question {
  z-index: 21000;
  width: 80%;
  height: 150px;
  margin-top: 140px;
  word-wrap: break-word;
  text-align: justify;
  vertical-align: middle;
  font-family: 'DungGeunMo';
  font-size: 1.6rem;
}

.choices {
  z-index: 21000;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  gap: 10px;
}

.choice-btns {
  width: 80%;
  max-width: 600px;
  min-width: 300px;
  height: auto;
  padding: 10px 20px;
  font-family: 'DungGeunMo';
  font-size: 1.1rem;
  line-height: 1.4;
  text-align: justify;
}

.question-image { 
  width: 100%;
  height: 100%;
}

button {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
 
button:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.month-select {
  width: 250px;
  height: 60px;
  padding: 10px;
  font-size: 1rem;
  font-family: 'DungGeunMo';
  font-size: 1.5rem;
}

.month-select > option {
  text-align: center;
}

textarea {
  width: 80%;
  height: 100px;
  padding: 10px 20px;
  font-size: 1.2rem;
  resize: none;
  font-family: 'DungGeunMo';
}

.result-container {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
}

.result-items {
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 20001;
}

.friend-name {
  position: absolute;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  top: -3px;
  left: 8%;
  width: 250px;
  text-align: right;
  font-family:'DNFBitBitv2';
  font-size: 2.3rem;
  color: #AD88C6;
  text-shadow: 
    2px 2px 0 #1f1f1f,  /* 오른쪽 아래 */
    -2px -2px 0 #1f1f1f, /* 왼쪽 위 */
    -2px 2px 0 #1f1f1f,  /* 왼쪽 아래 */
    2px -2px 0 #1f1f1f;  /* 오른쪽 위 */
}

.friend-title {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 60px;
  text-align: center;
  font-family: 'DungGeunMo';
  font-size: auto;
  color: #f8f8f8;
  text-shadow: 2px 2px 2px #1f1f1f;
}

.movie-rating {
  position: absolute;
  top: 130px;
  left: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.star {
  width: 20px;
  height: 20px;
  margin-right: 2px;
}

.desc-box {
  position: absolute;
  top: 220px;
  left: 5%;
  background-color: rgba(254, 254, 254, 0.7);
  border: 1px solid #1f1f1f;
  border-radius: 10px;
  width: 90%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DungGeunMo';
}

.desc-box > p > span {
  background-color: #AD88C6;
  padding: 3px;
}

.message-box {
  position: absolute;
  top: 300px;
  left: 20px;
  width: 300px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.message-box > img {
  position: relative;
  width: 100%;
  height: 100%;
  opacity: 0.8;
}

.message-box > p {
  position: absolute;
  top: -25px;
  left: 5px;
  z-index: 20002;
  width: 100%;
  height: 100%;
  padding: 30px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: justify;
  line-height: 1.6;
  font-family: 'DungGeunMo';
}

.pigtail {
  position: absolute;
  width: 100px;
  top: 500px;
  left: 40%;
  transform: scaleY(-1) rotate(30deg);
}

.friend-state {
  position: absolute;
  top: 580px;
  left: 24%;
  transform: rotate(20deg);
  font-family: 'UhBeeSeulvely';
  font-size: 2.8rem;
  color: #f8f8f8;
  text-shadow: 2px 2px 2px #1f1f1f;
}

.result-cat {
  position: absolute;
  width: 300px;
  top: 400px;
}

.result-bg {
  position: relative;
  z-index: 20000;
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  overflow: hidden;
}

.result-bg > img {
  width: 100%;
  height: 100%;
  min-width: 600px;
  min-height: 800px;
  position: relative;
}

.movie-poster-bg {
  position: absolute;
  right: 0;
  top: 50px;
  z-index: 19999;
  width: 450px;
  height: 700px;
}

.movie-poster-bg > img {
  width: 450px;
  height: 700px;
  object-fit: cover;
}

.buttons {
  width: 100%;
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 21000;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  align-items: center;
}

.buttons > button {
  width: 140px;
  height: 40px;
  background-color: #f8f8f8;
  font-family: 'DungGeunMo';
  font-size: 1.2rem;
}

.buttons > button:hover {
  background-color: #888;
}

.loading-status {
  background-color: #1f1f1f;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.load-message {
  font-family: 'S-CoreDream-3Light';
  color: #f8f8f8;
  text-align: center;
}

</style>