from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import CustomUserSerializer, MyPageSerializer, CustomUserUpdateSerializer
from django.contrib.auth.hashers import make_password # 유저 정보 임의 입력 후 해시화할 때 사용
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from urllib.parse import urlencode
import requests

from .models import User
from movies.models import Bookmark, Like
from community.models import Review, Comment, Movieforyou



# 유저 커스텀을 위한 클래스 뷰
class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer

# 유저 커스텀을 위한 클래스 뷰
class CustomUserInfoView(APIView):
  authentication_classes = [JWTAuthentication]  # JWT 인증
  permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

  def get(self, request):
    user = get_object_or_404(User, pk=request.user.pk)

    bookmarked_movies = Bookmark.objects.filter(user=user).values_list('id', flat=True)
    liked_movies = Like.objects.filter(user=user).values_list('id', flat=True)

    serializer = CustomUserSerializer(user)
    user_data = serializer.data
    user_data.update({
      'bookmarked_movies': list(bookmarked_movies),
      'liked_movies': list(liked_movies),
    })

    return Response(user_data)
  
  def patch(self, request):
    if not request.user or not request.user.is_authenticated:
      return Response({"detail": "로그인이 필요합니다."}, status=401)
    user = request.user
    serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# 회원가입을 위한 이메일 요청
# @api_view(['POST'])
# def resend_email_verification(request):
#   user = request.user
#   if not user.is_authenticated:
#     return Response({"detail": "로그인이 필요합니다."}, status=401)

#   try:
#     email_address = EmailAddress.objects.get(user=user, email=user.email)
#     if email_address.verified:
#       return Response({"detail": "이미 이메일 인증이 완료되었습니다."}, status=400)
#     email_address.send_confirmation(request)
#     return Response({"detail": "이메일 인증 메일이 전송되었습니다."}, status=200)
#   except ObjectDoesNotExist:
#     return Response({"detail": "유효하지 않은 사용자입니다."}, status=400)

# 카카오 로그인

class KakaoLogin(APIView):
    def get(self, request, *args, **kwargs):
        # Step 1: Authorization Code 받기
        auth_code = request.GET.get('code')
        if not auth_code:
            return Response({"error": "Authorization code is missing."}, status=400)

        # Step 2: Access Token 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.SOCIAL_AUTH_KAKAO_REST_ID,
            "client_secret": settings.SOCIAL_AUTH_KAKAO_CLIENT_SECRET_ID,
            "redirect_uri": "http://127.0.0.1:8000/accounts/kakao/login/callback/",
            "code": auth_code,
        }
        token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.post(token_url, data=token_data, headers=token_headers)

        if token_response.status_code != 200:
            return Response({"error": "Failed to get access token."}, status=token_response.status_code)

        access_token = token_response.json().get("access_token")

        # Step 3: 사용자 정보 요청
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        user_info_headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=user_info_headers)

        if user_info_response.status_code != 200:
            return Response({"error": "Failed to get user info."}, status=user_info_response.status_code)

        user_info = user_info_response.json()
        kakao_account = user_info.get("kakao_account", {})
        email = kakao_account.get("email", f"kakao_{user_info['id']}@kakao.com")
        nickname = kakao_account.get("profile", {}).get("nickname", f"kakao_{user_info['id']}")

        # Step 4: 유저 생성 또는 조회
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"nickname": nickname, "username": email.split("@")[0]},
        )

        # Step 5: JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        redirect_url = f"http://localhost:5173/login?access_token={access_token}&refresh_token={refresh}"
        return redirect(redirect_url)


    
def kakao_login_redirect(request):
    # 카카오 인증 URL 생성 및 리다이렉트
    kakao_auth_url = "https://kauth.kakao.com/oauth/authorize"
    client_id = settings.SOCIAL_AUTH_KAKAO_REST_ID
    redirect_uri = "http://127.0.0.1:5173/kakao/login/callback"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code"
    }
    redirect_url = f"{kakao_auth_url}?{urlencode(params)}"
    return redirect(redirect_url)


# 마이페이지 접근
@api_view(['GET'])
def mypage(request, username):
  person = get_object_or_404(User, username=username)
  serializer = MyPageSerializer(person)
  return Response(serializer.data)


# 회원 탈퇴
@api_view(['DELETE'])
def delete_user(request, user_id):
  if request.user.id != user_id:
    return Response({"detail": "해당 작업을 수행할 권한이 없습니다."}, status=403)
  user = get_object_or_404(User, id=user_id)
  user.delete()
  return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=204)
  

# 팔로우하기
@api_view(['POST'])
def follows(request, personname):
  person = get_object_or_404(User, username=personname)
  if request.user == person:
    return Response({"detail": "자기 자신은 팔로우할 수 없습니다."}, status=403)
  is_followed = person.followers.filter(pk=request.user.pk).exists()
  if is_followed:
    person.followers.remove(request.user)
  else:
    person.followers.add(request.user)
    
  return Response({"is_followed": not is_followed}, status=200)
  
  from django.contrib.auth.hashers import make_password

# 암호화되지 않은 더미유저 데이터를 암호화하는 경로
# @api_view(['GET'])
# def encrypt_all_passwords(request):
#     users = User.objects.all()

#     for user in users:
#         if not user.password.startswith("pbkdf2_"):  # 이미 암호화된 비밀번호는 제외
#             user.set_password(user.password)
#             user.save()

#     return Response({"detail": f"{users.count()}명의 비밀번호가 암호화되었습니다."}, status=200)
