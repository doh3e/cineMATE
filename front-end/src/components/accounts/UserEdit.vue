<template>
  <div class="user-edit-container">
    <h2>회원 정보 수정</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="nickname">닉네임</label>
        <input type="text" v-model="form.nickname" id="nickname" required />
      </div>
      <div>
        <label for="old_password">현재 비밀번호</label>
        <input type="password" v-model="form.old_password" id="old_password" required />
      </div>
      <div>
        <label for="new_password1">새 비밀번호</label>
        <input type="password" v-model="form.new_password1" id="new_password1" />
      </div>
      <div>
        <label for="new_password2">새 비밀번호 확인</label>
        <input type="password" v-model="form.new_password2" id="new_password2" />
      </div>
      <div>
        <label for="email">이메일</label>
        <input type="email" v-model="form.email" id="email" required />
      </div>
      <div>
        <label for="birthday">생일</label>
        <input type="date" v-model="form.birthday" id="birthday" />
      </div>
      <div>
        <label for="profile_image">프로필 이미지</label>
        <input type="file" @change="handleFileChange" id="profile_image" />
      </div>
      <button type="submit">저장</button>
    </form>
    <button @click="goodbye">회원탈퇴</button>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authAxios } from '@/axios'
import { useCounterStore } from '@/stores/counter'

const router = useRouter()
const route = useRoute()
const store = useCounterStore()


const form = reactive({
  email: '',
  nickname: '',
  birthday: '',
  profile_image: null,
  old_password: '',
  new_password1: '',
  new_password2: '',
})

// store에서 초기값 가져오기
onMounted(() => {
  if (store.userInfo) {
    form.email = store.userInfo.email || ''
    form.nickname = store.userInfo.nickname || ''
    form.birthday = store.userInfo.birthday || ''
  }
})

// 파일 선택 핸들러
const handleFileChange = (event) => {
  const file = event.target.files[0]
  form.profile_image = file
}

// 회원 탈퇴
const goodbye = async () => {
  if(route.params.username !== store.userInfo.username) {
    alert('탈퇴 권한이 없습니다!')
    return
  }
  const isReal = confirm('정말 회원 탈퇴를 하시겠어요?')
  if(isReal){
    try{
      await authAxios.delete(`/accounts/delete/${store.userInfo.id}`)
      alert('정상적으로 탈퇴 되었습니다.')
      store.logout()
    }
    catch(error) {
      console.error('회원 탈퇴 오류:', error.response?.data || error.message)
      alert('회원 탈퇴에 실패했습니다. 잠시 후 다시 시도해주세요.')   
    }
  }
}

// 회원 수정
const submitForm = async () => {
  if(route.params.username !== store.userInfo.username) {
    alert('수정 권한이 없습니다!')
    return
  }
  try {
    const formData = new FormData()
    for (const key in form) {
      if (form[key] !== null && form[key] !== '') {
        formData.append(key, form[key])
      }
    }

    await authAxios.patch('/accounts/dj-rest-auth/user/', formData)
    alert('회원 정보가 수정되었습니다.')

    // 사용자 정보 업데이트
    await store.getUserInfo()
    window.location.reload()
  } catch (error) {
    console.error('회원 정보 수정 오류:', error.response?.data || error.message)
    alert('회원 정보 수정에 실패했습니다. 입력 내용을 확인해주세요.')
  }
}
</script>

<style scoped>
.user-edit-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}
form div {
  margin-bottom: 15px;
}
button {
  display: block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
