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

from .models import User
from movies.models import Bookmark, Like
from community.models import Review, Comment, Movieforyou


class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer


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
    user = request.user
    serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def mypage(request, username):
  user = get_object_or_404(User, username=username)
  serializer = MyPageSerializer(user)
  return Response(serializer.data)


@api_view(['DELETE'])
def delete_user(request, user_id):
  if request.user.id != user_id:
    return Response({"detail": "권한이 없습니다."}, status=403)
  user = get_object_or_404(User, id=user_id)
  user.delete()
  return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=204)
  
  
@api_view(['POST'])
def follows(request, personname):
  user = get_user_model()
  person = get_object_or_404(User, username=personname)
  if request.user.username != person:
    if person.followers.filter(pk=request.user.pk).exists():
      person.followers.remove(request.user)
      is_followed = False
    else:
      person.followers.add(request.user)
      is_followed = True
    return Response({"is_followed": is_followed}, status=200)
  return Response({"detail": "자기자신은 팔로우 할 수 없습니다."}, status=403)
  
  