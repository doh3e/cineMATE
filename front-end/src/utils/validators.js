export const validateUsername = (username) => {
  const regex = /^[a-z0-9_]{4,15}$/
  return regex.test(username)
    ? ''
    : '아이디는 4~15글자, 영문 소문자, 숫자, _ 만 가능합니다.'
}

export const validateEmail = (email) => {
  const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
  return regex.test(email)
    ? ''
    : '유효한 이메일 주소를 입력해주세요.'
}

export const validatePassword = (password) => {
  const regex = /^(?=.*[a-zA-Z])(?=.*\d).{8,16}$/
  return regex.test(password)
    ? ''
    : '비밀번호는 8~16글자, 영문과 숫자를 혼용해야 합니다.'
}

export const validatePasswordMatch = (password1, password2) => {
  return password1 === password2
    ? ''
    : '비밀번호가 일치하지 않습니다.'
}

export const validateNickname = (nickname) => {
  const regex = /^[가-힣a-zA-Z0-9]{2,12}$/
  return regex.test(nickname)
    ? ''
    : '닉네임은 2~12글자, 한글, 영문 대소문자, 숫자만 가능합니다.'
}

export const validateBirthday = (birthday) => {
  if (!birthday) return ''
  const date = new Date(birthday)
  const now = new Date()
  const maxYear = now.getFullYear() - 200
  return date > now || date.getFullYear() < maxYear
    ? '생년월일은 미래이거나 현재 년도에서 200년 이상 차이날 수 없습니다.'
    : ''
}
