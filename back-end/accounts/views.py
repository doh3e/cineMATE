from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import CustomUserSerializer, MyPageSerializer, CustomUserUpdateSerializer
from django.contrib.auth.hashers import make_password # 유저 정보 임의 입력 후 해시화할 때 사용

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
