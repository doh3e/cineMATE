from rest_framework import serializers
from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)

class MovieDetailSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'overview', 'adult',
            'popularity', 'vote_average', 'genre_ids',
            'release_date', 'poster_path', 'youtube_path',
        ]
