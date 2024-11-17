from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from community.models import Review
from movies.models import Bookmark, Like


class CustomUserSerializer(UserDetailsSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'nickname', 'birthday', 'profile_image', 'date_joined', 'last_login']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['id'] = user.id
    token['username'] = user.username
    token['email'] = user.email
    token['nickname'] = user.nickname
    token['birthday'] = str(user.birthday) if user.birthday else None
    token['profile_image'] = user.profile_image.url if user.profile_image else None
    token['date_joined'] = str(user.date_joined) if user.date_joined else None
    token['last_login'] = str(user.last_login) if user.last_login else None
    return token


class MypageBookmarkSerializer(serializers.ModelSerializer):
  class Meta:
      model = Bookmark
      fields = [
        'id', 'title', 'overview', 'adult',
        'popularity', 'vote_average', 'genre_ids',
        'release_date', 'poster_path'
      ]


class MypageLikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = [
      'id', 'title', 'overview', 'adult',
      'popularity', 'vote_average', 'genre_ids',
      'release_date', 'poster_path'
    ]


class MypageReviewSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField(read_only=True)
  genre_names = serializers.SerializerMethodField()
  like_count = serializers.IntegerField(read_only=True)
  liked_users = serializers.SerializerMethodField()

  class Meta:
    model = Review
    fields = [
      'review_id', 'review_title', 'id', 'title', 'overview', 'adult',
      'popularity', 'vote_average', 'release_date', 'poster_path',
      'user_rating', 'review_content', 'created_at', 'updated_at', 'user',
      'genre_ids', 'genre_names', 'like_count', 'liked_users'
    ]
    read_only_fields = ('review_id', 'user', 'created_at', 'updated_at', 'like_count', 'liked_users',)

  def get_genre_names(self, obj):
    return [genre.name for genre in obj.genre_ids.all()]
  
  def get_liked_users(self, obj):
    return obj.likes.values_list('id', flat=True)


class MyPageSerializer(serializers.ModelSerializer):
  bookmarked_movies = serializers.SerializerMethodField()
  liked_movies = serializers.SerializerMethodField()
  my_reviews = MypageReviewSerializer(many=True, source='user_reviews')
  liked_reviews = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = [
      'id', 'username', 'email', 'nickname', 'birthday', 'profile_image',
      'date_joined', 'last_login', 'bookmarked_movies', 'liked_movies',
      'my_reviews', 'liked_reviews'
    ]

  def get_bookmarked_movies(self, obj):
    bookmarks = Bookmark.objects.filter(user=obj)
    return MypageBookmarkSerializer(bookmarks, many=True).data

  def get_liked_movies(self, obj):
    likes = Like.objects.filter(user=obj)
    return MypageLikeSerializer(likes, many=True).data
  
  def get_liked_reviews(self, obj):
    liked_reviews = Review.objects.filter(likes=obj)
    return MypageReviewSerializer(liked_reviews, many=True).data