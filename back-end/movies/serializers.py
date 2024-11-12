from rest_framework import serializers
from .models import Movie, Genre

class TopRatedMovieListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_title', 'poster_path', 'release_date', 'movie_rating',)
