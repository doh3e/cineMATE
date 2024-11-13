from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import CustomTokenObtainPairView, CustomUserInfoView


app_name = "accounts"
urlpatterns = [
    # 로그인, 로그아웃, 비밀번호 변경 등을 제공하는 dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/user/', CustomUserInfoView.as_view(), name='custom_user_info'),  # 커스텀 유저 정보
    # 회원가입 관련 URL
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # JWT 토큰 발급 및 갱신을 위한 URL 추가
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 커스텀 JWT 토큰 발급
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # JWT 토큰 갱신
]