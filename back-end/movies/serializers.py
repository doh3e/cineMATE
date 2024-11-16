from rest_framework import serializers
from .models import Movie, Genre, Bookmark, Like
from django.db.models import Count



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')  # 'name' 필드를 추가


class MovieDetailSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'overview', 'adult',
            'popularity', 'vote_average', 'genre_ids',
            'release_date', 'poster_path', 'bookmarks_count', 'likes_count'
        ]
