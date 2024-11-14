from rest_framework import serializers
from .models import Movie, Genre

class TopRatedMovieListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_title', 'poster_path', 'release_date', 'movie_rating',)


class MovieDetailSerializer(serializers.ModelSerializer):
  class GenreSerializer(serializers.ModelSerializer):
    class Meta:
      model = Genre
      fields = ('name',)
  
  def get_genres(self, obj):
    return self.GenreSerializer(obj.genres.all(), many=True).data
  
  class Meta:
    model = Movie
    fields = [
      'movie_code', 'movie_title', 'movie_overview', 'is_adult', 'movie_popularity', 
      'movie_rating', 'release_date', 'poster_path', 'bookmarks', 'genres'
    ]