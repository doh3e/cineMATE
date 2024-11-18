from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.password_validation import validate_password
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
    if user.profile_image and user.profile_image != "null":
      token['profile_image'] = user.profile_image.url
    else:
      token['profile_image'] = None
    token['date_joined'] = str(user.date_joined) if user.date_joined else None
    token['last_login'] = str(user.last_login) if user.last_login else None
    return token


class CustomUserUpdateSerializer(serializers.ModelSerializer):
  # 일반 정보 필드
  email = serializers.EmailField(required=True)
  nickname = serializers.CharField(required=True)
  birthday = serializers.DateField(required=False)
  profile_image = serializers.ImageField(required=False)

  # 비밀번호 필드
  old_password = serializers.CharField(write_only=True, required=False)
  new_password1 = serializers.CharField(write_only=True, required=False, validators=[validate_password])
  new_password2 = serializers.CharField(write_only=True, required=False)

  class Meta:
    model = User
    fields = ['email', 'nickname', 'birthday', 'profile_image', 'old_password', 'new_password1', 'new_password2']

  def validate(self, data):
    # 비밀번호 변경 관련 검증
    if data.get('new_password1') or data.get('new_password2'):
      # old_password가 없으면 에러
      if not data.get('old_password'):
        raise serializers.ValidationError({"old_password": "Old password is required to change the password."})
      # 새 비밀번호와 확인 비밀번호가 다르면 에러
      if data.get('new_password1') != data.get('new_password2'):
        raise serializers.ValidationError({"new_password2": "Passwords do not match."})
    return data

  def update(self, instance, validated_data):
    # 일반 정보 업데이트
    instance.email = validated_data.get('email', instance.email)
    instance.nickname = validated_data.get('nickname', instance.nickname)
    instance.birthday = validated_data.get('birthday', instance.birthday)
    instance.profile_image = validated_data.get('profile_image', instance.profile_image)

    # 비밀번호 변경
    if validated_data.get('old_password') and validated_data.get('new_password1'):
      # 기존 비밀번호 확인
      if not instance.check_password(validated_data['old_password']):
        raise serializers.ValidationError({"old_password": "Old password is incorrect."})
      # 새 비밀번호 설정
      instance.set_password(validated_data['new_password1'])

    instance.save()
    return instance


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
  followings = serializers.SerializerMethodField()
  followers = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = [
      'id', 'username', 'email', 'nickname', 'birthday', 'profile_image',
      'date_joined', 'last_login', 'bookmarked_movies', 'liked_movies',
      'my_reviews', 'liked_reviews', 'followings', 'followers',
    ]

  def get_bookmarked_movies(self, obj):
    bookmarks = Bookmark.objects.filter(user=obj)
    return MypageBookmarkSerializer(bookmarks, many=True).data

  def get_liked_movies(self, obj):
    likes = Like.objects.filter(user=obj)
    return MypageLikeSerializer(likes, many=True).data
 
  def get_my_reviews(self, obj):
      print("My Reviews:", obj.user_reviews.all())
      return MypageReviewSerializer(obj.user_reviews.all(), many=True).data
  
  def get_liked_reviews(self, obj):
    liked_reviews = Review.objects.filter(likes=obj)
    return MypageReviewSerializer(liked_reviews, many=True).data
  
  def get_followings(self, obj):
      followings = obj.followings.all()
      print(f"Followings for {obj.username}: {followings}")  # 디버깅 출력
      return [user.username for user in followings]

  def get_followers(self, obj):
      followers = obj.followers.all()
      print(f"Followers for {obj.username}: {followers}")  # 디버깅 출력
      return [user.username for user in followers]
