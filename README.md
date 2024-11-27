# 🎞 Your BEST movie friend, cineMATE 🎞

<div>씨네메이트(cineMATE)는 유저에게 딱 맞는 <code>영화를 추천</code> 해주고, <code>리뷰를 작성</code> 하기도 하며, 좋아하는 영화에 <code>좋아요</code> 할 수도, 보고 싶은 영화를 <code>북마크</code> 에 담아둘 수도 있고, 여러 선택지를 제시하는 테스트를 통해 <code>내 친구와 닮은 영화를 찾아주는</code> 등 재미난 기능이 많은 <img src="https://img.shields.io/badge/django-092E20?style=flat-square&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/vue.js-4FC08D?style=flat-square&logo=vue.js&logoColor=white"> 기반의 웹사이트입니다.</div><br>
<p>이 프로젝트는 SSAFY(Samsung Software Academy For Youth) 12기 비전공 파이썬 1학기 프로젝트입니다.</p>

<br>

## 🎥 시연 영상

[유튜브 링크](https://youtu.be/9zXQB_v5KVM)

<br>

## 🙋‍♀️ 팀원 정보 및 업무 분담 내역
|   Name   | 정지은 👑                         | 홍노을                                            | 
| :------: | ------------------------------------ | ------------------------------------------------- |
| Profile  |<p align="center"><img src="https://github.com/user-attachments/assets/49da79e2-1131-4e15-a7c2-dc04f29ca1e6" style="width:180px; height:220px; object-fit:cover;"></p>|<p align="center"><img src="https://github.com/user-attachments/assets/28c636e2-97ec-4302-acdb-f1fa9b8a4b8e" style="width:180px; height:220px; object-fit:cover;"></p>|
| Position | Front/Backend Develop  | Backend Develop                                  |
|   Git    | [@doh3e](https://github.com/doh3e) | [@H11-eng](https://github.com/H11-eng) |
|   E-mail    | wldms3333@gmail.com| hne9711@gmail.com|

<br>

<div>
  <code><b>정지은</b></code>
  <p>아이디어 구상 / 프로젝트 흐름 구상 / UX UI 디자인 / 테마 및 컨셉 아이디어 제시<br>
    모델 정의 및 ERD 생성 / Django allauth, dj-rest-auth, simpleJWT 기반의 회원가입 및 로그인 로직 <br>
    메인 페이지, 영화 파트 백엔드 로직 제작 및 프론트 작업 전반 <br>
    회원 파트 (로그인, 회원가입, 마이페이지) 로직 제작 및 프론트 작업 전반 <br>
    리뷰 파트 프론트, CSS 작업 / 무비포유(친구와 닮은 영화 찾기) 로직 및 프론트, 이미지 작업 <br>
    깃허브 유지보수 / 백업 관리
  </p>
</div>
<div>
  <code><b>홍노을</b></code>
  <p>아이디어 구상 / 프로젝트 흐름 구상 / 모델 정의 / 테마 및 컨셉 아이디어 제시<br>
  Django DRF 기반 Serializer 작성 / Review, Comment CRUD 작성<br>
  디버깅 / 프레젠테이션 작업 / fixture 및 DB 관리</p>
</div>
<br>

## 🔧 목표 서비스 구현 및 실제 구현 정도
  
  ### 구현 목표
  
  1. 관통프로젝트 필수 요구사항 이행 (영화 DB, 추천기능, 커뮤니티)<br>
  2. back-end에 <code>Django</code> / front-end에 <code>Vue.js</code> 를 활용하여 반응형 웹페이지 제작 <br>
  3. 디자인과 컨셉 : <code>우주</code>, <code>코스믹</code> 그리고 <code>고양이</code> 한 스푼. <br>
    * 디자인 및 컨셉의 통일성 확보 <br>
  4. 영화 API를 활용하여 영화 검색, 추천 기능 활성화 <br>
    * 최소 3가지 유형으로 추천받을 수 있도록 함 <br>
    * 유저의 선호 기반 추천 알고리즘을 제시하려고 노력 <br>
  5. 리뷰 작성 시에도 API를 호출하여 유저가 영화 제목만 검색하면 정확한 영화 정보가 다 기입될 수 있도록 함 <br>
    * 리뷰 댓글, 좋아요 기능 <br>
  6. 간단한 테스트를 제공하여 유저가 자신의 친구들에게 '자신이 생각한 친구와 닮은 영화'를 공유할 수 있도록 함 <br>
    * 사이트 방문 유도, 흥미 요소 부여 <br>
    * 자신이 만든 친구 카드를 PC와 서버에 저장 <br><br>

  ### 실제 구현 수준

  1. **필수 요구사항 이행 완료**
     - [x] 회원 기능(회원가입/로그인 등), 영화 DB fixture 2000개, 여러가지 추천 기능 구현,<br>
      - [x] 유저간의 소통이 가능한 리뷰 게시판 및 상호 팔로우가 가능한 환경 구축 <br>
  
  2. **프론트-백 간의 원활한 흐름, 유저의 화면 크기에 따른 반응형 웹페이지 구현**
     - [x] bootstrap을 활용하지 않고 순수 css로 media 쿼리를 작성하여 모바일 환경까지는 고려하기 어려웠으나,<br>
       PC나 태블릿 환경의 유저가 비슷한 경험을 할 수 있도록 고려하여 화면 배치<br>
     - [x] back-end와 front-end의 원활한 상호작용 확인. 오류가 날 시 상황에 맞는 오류 메세지를 throw / catch 하도록 고려
  3. **유저가 직관적으로 파악할 수 있도록 UX/UI 통일 고려, 디자인 컨셉 통일감 중시**
     - [x] 사용 font와 color 등을 사전에 지정하여 가급적이면 해당 무드를 벗어나지 않도록 함
     - [x] 동시에 정적이고 딱딱한 사이트가 아니라 최대한 유저가 다양한 경험을 하고 즐길 수 있도록 애니메이션 등 활성화<br>
  
  4. **영화 API를 통해 유저가 영화를 검색하기 용이하게 하고, 받아온 API를 백엔드에서 여러 알고리즘으로 처리하여 다양한 추천 제시**
     - [x] 사용 API : TMDB, KOFIC(영화진흥위원회 DB)
     - [x] 추천 로직에 관해서는 추천 로직 설명 파트에서 자세히 다룸
  5. **리뷰 작성 시 정확한 정보를 유저가 입력하게 하기 보다는, 간단한 검색으로 영화 정보를 전부 받아올 수 있게 리뷰 작성 페이지 구현**
  6. **<code>무비포유</code> 테스트 제작, 저장 성공**
     - [x] 주변 친구들에게 테스트 시켜본 결과 반응이 좋았음 <br>
     <br>


## 💾 데이터베이스 모델링(ERD)
<br>

![cineMATE](https://github.com/user-attachments/assets/cd5282aa-0938-4081-abc2-500f104d4403)

<br>
<code><b>Like, Bookmark가 manytomany가 되지 않은 이유</b></code><br><br>
<p>
  DB에 있는 영화는 2000개에 불과한데, API를 통한 검색으로도 영화를 찾고 북마크/좋아요 할 수 있기 때문<br>
  DB에 없는 영화를 manytomany로 연결할 순 없다! => 두 모델에 영화 정보를 함께 추가하게 된 이유이기도 함
</p><br>

## 🖥 프로젝트 구조
```
cineMATE/
├─ back-end/
│  ├─ accounts/           회원관리
│  ├─ cinemate/           프로젝트 설정
│  ├─ community/          커뮤니티
│  ├─ media/              유저 업로드 폴더
│  ├─ movies/             영화관련 기능
│  └─ requirements.txt    백엔드 의존성 파일
├─ front-end/
│  ├─ index.html
│  ├─ package.json       
│  └─ src/
│     ├─ App.vue
│     ├─ assets/          정적 리소스용 폴더(CSS, img)
│     ├─ axios.js         백엔드 비동기요청용 js 파일
│     ├─ components/      vue 하위컴포넌트 폴더
│     │  ├─ accounts/     회원 관련 하위컴포넌트
│     │  ├─ community/    커뮤니티 관련 하위컴포넌트
│     │  ├─ movies/       영화 관련 하위컴포넌트
│     │  └─ Navbar.vue    네비게이션 바
│     ├─ main.js
│     ├─ router
│     │  └─ index.js
│     ├─ stores
│     │  └─ counter.js
│     ├─ utils
│     │  └─ validators.js 회원 유효성검사용 js 파일
│     └─ views            vue 상위 컴포넌트 폴더 (라우터에 직접연결됨)
├─ project_resource       프로젝트 내에서 필요한 리소스 모음
└─ README.md
```

<br>

## 🎬 영화 추천 알고리즘에 대한 기술적 설명

### 메인화면의 Top rated
<p>사전에 인기순으로 불러온 2000개의 DB중 vote_average(평점, 10점 만점)와 vote_count(투표수)를 고려하여 100위 선정 후 보여줌</p>
<br>

### 영화 큐레이팅 페이지

<code><b>기본 추천 (좋아요/북마크 기반)</b></code><br>
<p>유저가 좋아요/북마크 한 영화의 장르 중 가장 많은 장르 1, 2위를 뽑고 1, 2위 장르가 함께 포함된 영화를 찾는다.</p>
<img src="https://github.com/user-attachments/assets/65ff2283-d464-4973-93d8-064493fd0b3b" width=900>
<img src="https://github.com/user-attachments/assets/0fe4b454-ffff-4abb-8964-6ace3fedd91d" width=900>
<br><br>
<code><b>특별한 날 추천(생일, 크리스마스 등...)</b></code><br>
<p>생일, 혹은 개발자가 지정해둔 특별한 날에 관련 큐레이션을 띄운다.</p>
<img src="https://github.com/user-attachments/assets/8dd58157-df47-4ef8-8ada-72f412b21025" width=900>
<img src="https://github.com/user-attachments/assets/9ebf25b5-3adc-4bb4-b022-83de6b09bb63" width=900>
<br><br>
<code><b>유사유저 기반 추천</b></code><br>
<p>나와 선호하는 영화가 비슷한 유저 상위 몇 명을 뽑아 유사유저로 지정하고, 유사유저가 좋아하거나 북마크한 다른 영화를 추천한다.</p>
<img src="https://github.com/user-attachments/assets/612ea7e6-bfd2-473a-87e5-a886f193cdc0" width=900>
<img src="https://github.com/user-attachments/assets/102f7ac8-70a3-4547-b7f6-a2cb769052e2" width=900>
<br><br>

## 🎮 핵심 기능에 대한 설명

  ### 메인화면
  <p>TOP RATED 영화 리스트, 국내 박스오피스 순위 및 신작 목록</p>
  <div>
    <img src="https://github.com/user-attachments/assets/fd4d31e1-b86f-4b77-aa38-65a738811766" width=900>
  </div> <br>
  
  ### 회원가입 및 로그인
  <p>회원가입 유효성 검사, 프로필사진 미리보기, 로그인, 로그아웃</p>
  <div>   
    <img src="https://github.com/user-attachments/assets/01946c6e-7d73-4984-989d-2ecdec8d1c4a" width=300>
    <img src="https://github.com/user-attachments/assets/3d200e5d-5a98-43f5-b222-6b1d5e44dddb" width=300>
    <img src="https://github.com/user-attachments/assets/a2516f0d-77df-441e-9d8e-f3df786ccba5" width=300>
  </div> <br>

  ### 마이페이지
  <p>내 정보 보기, 회원수정/탈퇴, 내 좋아요/북마크 저장함, 리뷰 보관함</p>
  <div>
    <img src="https://github.com/user-attachments/assets/6639b60e-f106-4a36-8681-407440d77880" width=900>
  </div> <br>

  ### 영화탐색
  <p>영화 장르별 보기, 영화 검색, 영화 큐레이팅, 영화 상세보기</p>
  <div>
    <img src="https://github.com/user-attachments/assets/407db785-9927-4113-bd60-a71ad1c71340" width=900>
    <img src="https://github.com/user-attachments/assets/6866ef91-8437-4838-b4da-8562531a0fbe" width=900>
    <img src="https://github.com/user-attachments/assets/f4e96e3c-03dd-4d2a-9599-a5fbc2f9b2fa" width=900>
    <img src="https://github.com/user-attachments/assets/65cfc9cf-b1ab-4df3-9bf5-d2cc3e112f15" width=900>
  </div> <br>

  ### 리뷰페이지
  <p>리뷰 게시판, 리뷰 작성, 리뷰 상세보기, 댓글</p>
  <div>
    <img src="https://github.com/user-attachments/assets/37d9dda5-ff90-4f68-a15f-604687213ce2" width=900>
    <img src="https://github.com/user-attachments/assets/e7655d81-ce0a-4427-8565-f2049e34145d" width=900>
  </div> <br>

  ### 무비포유
  <p>친구와 닮은 영화 찾기 테스트, 결과 파일로 저장 및 서버에 저장</p>
  <div>
    <img src="https://github.com/user-attachments/assets/f5f44d29-a336-44d1-8fa5-8b9020f39c90" width=300>
    <img src="https://github.com/user-attachments/assets/a0d8c10f-9372-45e7-82e2-b9cf51443c29" width=300>
    <img src="https://github.com/user-attachments/assets/df031e66-3f23-4149-875c-0ad167a5e180" width=300>
  </div>

<br>

## 📈 생성형 AI를 활용한 부분

### 테스트에서의 장르 가중치 계산 및 재분배, 리뷰 데이터 생성에 활용
<br>
<div>
  <img src="https://github.com/user-attachments/assets/93d907c4-5832-4aa5-9b5e-6a1b911c3251" width=900>
  <img src="https://github.com/user-attachments/assets/881bdea6-9eee-42f8-a341-cb319040bda2" width=900>
</div>

<br>

## 🎀 느낀 점과 후기

<code><b>정지은</b></code><br>
<p>
이번 프로젝트를 통해 백엔드와 프론트엔드를 모두 다뤄볼 수 있어 좋았다.<br>
또 UX를 어떻게하면 불편없이 짤 수 있을지에 대한 고민을 많이 해보는 시간이 되었다.<br>
몇 개월 전 외부에서 처음 해본 팀 프로젝트와 비교했을 때, 스스로 많이 성장했음을 느꼈다.<br>
다음에 프로젝트를 한다면 기능 하나하나의 깊이를 좀 더 파고들어보고 싶고,<br>
디자인패턴 등을 열심히 공부하여 좀 더 객체지향의 이점을 살린 프로그래밍을 해보고 싶다.<br>
</p>

<code><b>홍노을</b></code><br>
<p>
비전공자로서 SSAFY를 통해 처음으로 파이썬을 포함하여 알고리즘, 백엔드, 프론트엔드에 대해 배울 수 있었고,<br>
이번 기회로 RESTful한 백엔드 API 구현을 해볼 수 있어서 좋았다.<br>
한 학기동안 배운 내용을 바탕으로 유의미한 결과물을 만들어낼 수 있는 좋은 기회였다.<br>
</p>

<br>

## ⚙ 배포 서버 URL (배포했을 경우)

<p><b>추후 추가 예정</b></p>