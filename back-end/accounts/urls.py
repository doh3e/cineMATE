from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import CustomTokenObtainPairView, CustomUserInfoView


app_name = "accounts"
urlpatterns = [
    path('dj-rest-auth/user/', CustomUserInfoView.as_view(), name='custom_user_info'),  # 커스텀 유저 정보
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 커스텀 JWT 토큰 발급
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # JWT 토큰 갱신
]