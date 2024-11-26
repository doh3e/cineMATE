<template>
  <div class="sections-menu">
    <span class="menu-point" v-bind:class="{active: activeSection == index}" v-on:click="scrollToSection(index)" v-for="(offset, index) in offsets" v-bind:key="index" :title="'Go to section ' + (index+1)">
    </span>
  </div>
  <section class="fullpage black">
    <h3 class="goHome" @click="gotoMain">건너뛰기 →</h3>
    <h1>CINEMATE에 처음 접속하시나요?</h1>

  </section>
  <section class="fullpage black">
    <h1>Section 2</h1>
    <p>made with <a href="https://vuejs.org/" target="_blank">Vue.js</a></p>
  </section>
  <section class="fullpage red">
    <h1>Section 3</h1>
    <p>works on <span><b>desktop & mobile</b></span> devices</p>
  </section>
  <section class="fullpage purple">
    <h1>Section 4</h1>
    <p>tested in all <span><b>modern browsers</b></span></p>
  </section>
  <section class="fullpage green">
    <h1>Section 5</h1>
    <p>check the tutorial <a href="https://webdeasy.de/en/programming-vue-js-fullpage-scroll/?referer=cp-NVOEBL" target="_blank">here</a></p>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()

const inMove = ref(false)
const activeSection = ref(0)
const offsets = ref([])
const touchStartY = ref(0)
const inMoveDelay = 400

// 섹션 오프셋 계산
const calculateSectionOffsets = () => {
  const sections = document.getElementsByTagName('section')
  offsets.value = Array.from(sections).map(section => section.offsetTop)
}

// 섹션 스크롤 함수
const scrollToSection = (id, force = false) => {
  if (inMove.value && !force) return
  activeSection.value = id
  inMove.value = true

  const section = document.getElementsByTagName('section')[id]
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }

  setTimeout(() => {
    inMove.value = false
  }, inMoveDelay)
}

// 위로 이동
const moveUp = () => {
  if (inMove.value) return
  if (activeSection.value === offsets.value.length - 1) return
  inMove.value = true
  activeSection.value++

  if (activeSection.value >= offsets.value.length) {
    activeSection.value = 0
  }
  scrollToSection(activeSection.value, true)
}

// 아래로 이동
const moveDown = () => {
  if (inMove.value) return
  if (activeSection.value === 0) return
  inMove.value = true
  activeSection.value--

  if (activeSection.value < 0) {
    activeSection.value = offsets.value.length - 1
  }
  scrollToSection(activeSection.value, true)
}


// 마우스 휠 이벤트 처리
const handleMouseWheel = e => {
  if (e.wheelDelta > 0 && !inMove.value) {
    moveDown()
  } else if (e.wheelDelta < 0 && !inMove.value) {
    moveUp()
  }
  e.preventDefault()
}

// 터치 시작 이벤트 처리 (모바일)
const touchStart = e => {
  e.preventDefault()
  touchStartY.value = e.touches[0].clientY
}

// 터치 이동 이벤트 처리 (모바일)
const touchMove = e => {
  if (inMove.value) return
  e.preventDefault()

  const currentY = e.touches[0].clientY
  if (touchStartY.value < currentY) {
    moveDown()
  } else {
    moveUp()
  }
  touchStartY.value = 0
}

const gotoMain = () => {
  router.replace({name: 'Home'})
}

onMounted(() => {
  calculateSectionOffsets()

  window.addEventListener('mousewheel', handleMouseWheel, { passive: false }) // 브라우저
  window.addEventListener('DOMMouseScroll', handleMouseWheel, { passive: false }) // Firefox
  window.addEventListener('touchstart', touchStart, { passive: false }) // 모바일
  window.addEventListener('touchmove', touchMove, { passive: false }) // 모바일
})

onUnmounted(() => {
  window.removeEventListener('mousewheel', handleMouseWheel)
  window.removeEventListener('DOMMouseScroll', handleMouseWheel)
  window.removeEventListener('touchstart', touchStart)
  window.removeEventListener('touchmove', touchMove)
})


</script>

<style scoped>

body {
  margin: 0;
  color: #FFF;
  font-family: Helvetica, arial, sans-serif;
  overflow: hidden;
}

h2 {
  position: fixed;
}

.fullpage {
  position: relative;
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

h1 {
  color: #f8f8f8;
  font-size: 6em;
  margin: 0;
  text-align: center;
  padding: 0 1rem;
}

.goHome {
  position: absolute;
  color: #f8f8f8;
  top: 5%;
  right: 5%;
}

p {
  font-size: 1em;
}

.fullpage a, .fullpage span {
  text-decoration: none;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  color: #FFF;
  margin-left: 5px;
}

.red {
  background-color: #ab4545;
}

section.black {
  background-color: #000;
}

.blue {
  background-color: #237ad4;
}

.green {
  background-color: #5E9F6D;
}

.purple {
  background-color: #42325B;
}

h1.black {
  color: #000;
}

.sections-menu {
  position: fixed;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
}

.sections-menu .menu-point {
  width: 10px;
  height: 10px;
  background-color: #FFF;
  display: block;
  margin: 1rem 0;
  opacity: .6;
  transition: .4s ease-in-out all;
  cursor: pointer;
}

.sections-menu .menu-point.active {
  opacity: 1;
  transform: scale(1.5);
}

.sections-menu .menu-point:hover {
  opacity: 1;
  transform: scale(1.2);
}

@media screen and (max-width: 1200px) {
  h1 {
    font-size: 2.5em;
  }
}

</style>