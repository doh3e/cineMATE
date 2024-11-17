from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import CustomUserSerializer, MyPageSerializer

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


@api_view(['GET'])
def mypage(request, username):
  user = get_object_or_404(User, username=username)
  serializer = MyPageSerializer(user)
  return Response(serializer.data)

