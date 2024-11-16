from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer

from .models import User
from movies.models import Bookmark, Like


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserInfoView(APIView):
    authentication_classes = [JWTAuthentication]  # JWT 인증
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)

        bookmarked_movies = Bookmark.objects.filter(user=user).values_list('movie_id', flat=True)
        liked_movies = Like.objects.filter(user=user).values_list('movie_id', flat=True)

        serializer = CustomUserSerializer(user)
        user_data = serializer.data
        user_data.update({
            'bookmarked_movies': list(bookmarked_movies),
            'liked_movies': list(liked_movies),
        })

        return Response(user_data)
