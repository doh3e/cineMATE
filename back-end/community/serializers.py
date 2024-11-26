from rest_framework import serializers
from .models import Review, Comment, Movieforyou
from movies.models import Genre
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'username', 'nickname')


class ListReviewSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  like_count = serializers.IntegerField(read_only=True)
  comment_count = serializers.IntegerField(read_only=True)

  class Meta:
    model = Review
    fields = ('review_id', 'review_title', 'title', 'user', 'user_rating', 'created_at',
              'like_count', 'comment_count',)
    read_only_fields = ('review_id', 'user', 'created_at', 'like_count', 'comment_count',)


class ReviewSerializer(serializers.ModelSerializer):
  genre_ids = serializers.ListField(
    child=serializers.IntegerField(),
    write_only=True
  )
  class Meta:
    model = Review
    fields = [
      'review_id', 'review_title', 'id', 'title', 'overview', 'adult',
      'popularity', 'vote_average', 'genre_ids', 'release_date', 'poster_path',
      'user_rating', 'review_content', 
    ]

  def create(self, validated_data):
    genre_ids = validated_data.pop('genre_ids', [])
    review = super().create(validated_data)
    genres = Genre.objects.filter(id__in=genre_ids)
    review.genre_ids.set(genres)
    return review


class ReviewDetailSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
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
  
  def update(self, instance, validated_data):
    genre_ids = validated_data.pop('genre_ids', [])
    for attr, value in validated_data.items():
      setattr(instance, attr, value)
    instance.save()

    if genre_ids:
      genres = Genre.objects.filter(id__in=genre_ids)
      instance.genre_ids.set(genres)

    return instance


class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ('user', 'created_at', 'updated_at', 'review',) 

class MovieforyouSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movieforyou
    fields = '__all__'
    read_only_fields = ('user',) 


