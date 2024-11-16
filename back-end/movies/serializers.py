from rest_framework import serializers
from .models import Movie, Genre, Bookmark, Like


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id',)


class MovieDetailSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True)
    bookmarks_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'overview', 'adult',
            'popularity', 'vote_average', 'genre_ids',
            'release_date', 'poster_path', 'bookmarks_count', 'likes_count'
        ]

    def get_bookmarks_count(self, obj):
        # 해당 영화에 대한 북마크 수를 계산
        return Bookmark.objects.filter(movie_id=obj.id).count()

    def get_likes_count(self, obj):
        # 해당 영화에 대한 좋아요 수를 계산
        return Like.objects.filter(movie_id=obj.id).count()