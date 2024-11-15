from rest_framework import serializers
from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id',)


class TopRatedMovieListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_title', 'poster_path', 'release_date', 'movie_rating',)


class MovieDetailSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'movie_code', 'movie_title', 'movie_overview', 'is_adult',
            'movie_popularity', 'movie_rating', 'release_date',
            'poster_path', 'bookmarks', 'genres'
        ]