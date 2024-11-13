from django.urls import path, include
from . import views


app_name = "accounts"
urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경 등을 제공
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입을 포함
]