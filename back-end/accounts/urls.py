from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views
from .views import CustomTokenObtainPairView, CustomUserInfoView

app_name = "accounts"
urlpatterns = [
    path('dj-rest-auth/user/', CustomUserInfoView.as_view(), name='custom_user_info'),  # 커스텀 유저 정보
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 커스텀 JWT 토큰 발급
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # JWT 토큰 갱신

    path('checkid/<str:username>/', views.checkid, name="checkid"),
    path('mypage/<str:username>/', views.mypage, name='mypage'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('follows/<str:personname>/', views.follows, name='follows'),
    # path('hashing_user/', views.encrypt_all_passwords, name="hashing"), 암호화되지 않은 더미유저 데이터를 암호화하는 경로
]