<template>
  <div class="test-container">
    <!-- 이름 입력 단계 -->
    <div class="test-box" v-if="currentStep === -1">
      <div class="testimg start-img">
        <img src="@/assets/img/mvforyou-logo.png" alt="test-logo" class="test-logo">
        <h2 class="qname">{{ typedText }}<span v-if="showCaret" class="caret">_</span></h2>
        <input v-model="friendName" type="text" placeholder="이름 또는 별명 입력" />
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
      <div class="result-container">
        <div class="result-items">
          <h3 class="resultimp fname">{{ resultData?.my_choice.friend_name }}</h3>
          <p><strong>최고 장르:</strong> {{ resultData?.my_choice.top_genre }}</p>
          <p><strong>취향:</strong> {{ resultData?.my_choice.preference }}</p>
          <p><strong>태어난 달:</strong> {{ resultData?.my_choice.birth_month }}</p>
          <p><strong>메시지:</strong> {{ resultData?.my_choice.final_message }}</p>
          <h3>추천 영화</h3>
          <p><strong>제목:</strong> {{ resultData?.movie.title }}</p>
          <p><strong>개봉일:</strong> {{ resultData?.movie.release_date }}</p>
          <p><strong>평점:</strong> {{ resultData?.movie.vote_average }}</p>
        </div>
        <div class="backgroundimg result-bg">
          <img src="@/assets/img/test-result.png" alt="result-background">
        </div>
        <div class="movie-poster-bg">
          <img :src="store.getImageUrl(resultData?.movie.poster_path)" alt="poster">
        </div>
      </div>

      <!-- 버튼들 -->
      <div class="buttons">
        <button @click="saveResult">결정 및 저장하기</button>
        <button @click="retryTest">다시하기</button>
        <button @click="shareResult">공유하기</button>
      </div>
    </div>

    <!-- 로딩 화면 -->
    <div v-else-if="isLoading">
      <h2>결과를 불러오는 중...</h2>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
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
      { text: '사람들이 좋아하는 건 다 좋아해!', genres: { 드라마: 2, 로맨스: 2, 가족: 2, 액션: 2, 코미디: 2, 모험: 2, 음악: 2 }, preference: '다좋아' },
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
      { text: '강심장!', genres: { 공포: 3, 스릴러: 3, 액션: 3, 범죄: 2, 미스터리: 2, 모험: 1 }, preference: '강심장' },
      { text: '새가슴!', genres: { 드라마: 3, 가족: 3, 로맨스: 2, 음악: 2, 다큐멘터리: 2, 판타지: 1, SF: 1 }, preference: '새가슴' },
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
  console.log(chosenPreference.value)
  nextStep()
}

const nextStep = () => {
  currentStep.value++
}

const submitResults = async () => {
  const topGenre = Object.keys(genreScores.value).reduce((a, b) =>
    genreScores.value[a] > genreScores.value[b] ? a : b
  )

  console.log('가장 높은 점수의 장르:', topGenre)
  console.log('점수:', genreScores.value)
  console.log('메세지:', finalMessage)

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
    console.log('결과 전송 성공:', resultData.value)
  } catch (error) {
    console.error('결과 전송 실패:', error)
  } finally {
    isLoading.value = false // 로딩 종료
  }
}

const saveResult = () => {
  alert('결과가 저장되었습니다!')
}

const retryTest = () => {
  resultData.value = null
  currentStep.value = -1
  friendName.value = ''
  birthMonth.value = ''
  finalMessage.value = ''
  genreScores.value = {}
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
  width: 200px;
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
  position: absolute;
  z-index: 20001;
}

.resultimp .fname {
  position: absolute;
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
  z-index: 19999;
  width: 450px;
  height: 600px;
}

.movie-poster-bg > img {
  width: 450px;
  height: 600px;
  object-fit: cover;
}

.buttons {
  position: absolute;
  bottom: 50px;
  z-index: 21000;
  display: flex;
  gap: 10px;
  justify-content: center;
}


</style>