# 🎞 Your BEST movie friend, cineMATE 🎞

<div>씨네메이트(cineMATE)는 유저에게 딱 맞는 <code>영화를 추천</code> 해주고, <code>리뷰를 작성</code> 하기도 하며,<br>
  좋아하는 영화에 <code>좋아요</code> 할 수도, 보고 싶은 영화를 <code>북마크</code> 에 담아둘 수도 있고,<br>
  여러 선택지를 제시하는 테스트를 통해 <code>내 친구와 닮은 영화를 찾아주는</code> 등 재미난 기능이 많은
  <img src="https://img.shields.io/badge/django-092E20?style=flat-square&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/vue.js-4FC08D?style=flat-square&logo=vue.js&logoColor=white">
  기반의 웹사이트입니다.</div>

## SSAFY 12th 비전공 1학기 관통 프로젝트 : 영화


### 1. 팀원 정보 및 업무 분담 내역
|   Name   | 정지은 👑                         | 홍노을                                            | 
| :------: | ------------------------------------ | ------------------------------------------------- |
| Profile  |<p align="center"><img src="https://github.com/user-attachments/assets/49da79e2-1131-4e15-a7c2-dc04f29ca1e6" style="width:180px; height:220px; object-fit:cover;"></p>|<p align="center"><img src="https://github.com/user-attachments/assets/28c636e2-97ec-4302-acdb-f1fa9b8a4b8e" style="width:180px; height:220px; object-fit:cover;"></p>|
| Position | Front/Backend Develop  | Backend Develop                                  |
|   Git    | [@doh3e](https://github.com/doh3e) | [@H11-eng](https://github.com/H11-eng) |
|   E-mail    | wldms3333@gmail.com| hne9711@gmail.com|

<br>

#### 업무 분담
<div>
  <code><b>정지은</b></code>
</div>
<div>
  <code><b>홍노을</b></code>
</div>


### 2. 목표 서비스 구현 및 실제 구현 정도

<div>
  
  #### 구현 목표
  
  1. 관통프로젝트 필수 요구사항 이행 (영화 DB, 추천기능, 커뮤니티)
  2. back-end에 <code>Django</code> / front-end에 <code>Vue.js</code> 를 활용하여 반응형 웹페이지 제작
  3. 디자인과 컨셉 : <code>우주</code>, <code>코스믹</code> 그리고 <code>고양이</code> 한 스푼.
     - 디자인 및 컨셉의 통일성 확보
  4. 영화 API를 활용하여 영화 검색, 추천 기능 활성화
     - 최소 3가지 유형으로 추천받을 수 있도록 함
     - 유저의 선호 기반 추천 알고리즘을 제시하려고 노력
  5. 리뷰 작성 시에도 API를 호출하여 유저가 영화 제목만 검색하면 정확한 영화 정보가 다 기입될 수 있도록 함
     - 리뷰 댓글, 좋아요 기능
  6. 간단한 테스트를 제공하여 유저가 자신의 친구들에게 '자신이 생각한 친구와 닮은 영화'를 공유할 수 있도록 함
     - 사이트 방문 유도, 흥미 요소 부여
     - 자신이 만든 친구 카드를 PC와 서버에 저장

  #### 실제 구현 수준

  1. 필수 요구사항 이행 완료
     - 회원 기능(회원가입/로그인 등), 영화 DB fixture 2000개, 여러가지 추천 기능 구현,<br>
       유저간의 소통이 가능한 리뷰 게시판 및 상호 팔로우가 가능한 환경 구축 <br>

  <code><b>회원가입 및 로그인</b></code><br>
  <div>   
    <img src="https://github.com/user-attachments/assets/01946c6e-7d73-4984-989d-2ecdec8d1c4a" width=200>
    <img src="https://github.com/user-attachments/assets/3d200e5d-5a98-43f5-b222-6b1d5e44dddb" width=200>
    <img src="https://github.com/user-attachments/assets/a2516f0d-77df-441e-9d8e-f3df786ccba5" width=200>
  </div> <br>
  2. 프론트-백 간의 원활한 흐름, 유저의 화면 크기에 따른 반응형 웹페이지 구현
     - bootstrap을 활용하지 않고 순수 css로 media 쿼리를 작성하여 모바일 환경까지는 고려하기 어려웠으나,<br>
       PC나 태블릿 환경의 유저가 비슷한 경험을 할 수 있도록 고려하여 화면 배치
     - back-end와 front-end의 원활한 상호작용 확인. 오류가 날 시 상황에 맞는 오류 메세지를 throw / catch 하도록 고려
  3. 유저가 직관적으로 파악할 수 있도록 UX/UI 통일 고려, 디자인 컨셉 통일감 중시
     - 사용 font와 color 등을 사전에 지정하여 가급적이면 해당 무드를 벗어나지 않도록 함
     - 동시에 정적이고 딱딱한 사이트가 아니라 최대한 유저가 다양한 경험을 하고 즐길 수 있도록 애니메이션 등 활성화
  4. 영화 API를 통해 유저가 영화를 검색하기 용이하게 하고, 받아온 API를 백엔드에서 여러 알고리즘으로 처리하여 다양한 추천 제시
     - 사용 API : TMDB, KOFIC(영화진흥위원회 DB)
     - 추천 로직에 관해서는 추천 로직 설명 파트에서 자세히 다룸
  5. 리뷰 작성 시 정확한 정보를 유저가 입력하게 하기 보다는, 간단한 검색으로 영화 정보를 전부 받아올 수 있게 리뷰 작성 페이지 구현
     


### 3. 데이터베이스 모델링(ERD)
<br>

![cineMATE](https://github.com/user-attachments/assets/cd5282aa-0938-4081-abc2-500f104d4403)



### 4. 영화 추천 알고리즘에 대한 기술적 설명
### 5. 핵심 기능에 대한 설명
### 6. 생성형 AI를 활용한 부분
### 7. 기타 (느낀점, 후기 등)
### 8. 배포 서버 URL (배포했을 경우)
### 9. 이외의 내용은 자유롭게 작성 가능
