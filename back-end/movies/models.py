from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50)
    

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    adult = models.BooleanField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    genre_ids = models.ManyToManyField(Genre)
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)


class ActionBase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # 추상 클래스 (테이블 생성 안 함)
        unique_together = ('user', 'movie_id')


class Bookmark(ActionBase):
    """북마크 모델"""
    class Meta(ActionBase.Meta):
        db_table = 'movies_bookmark'


class Like(ActionBase):
    """좋아요 모델"""
    class Meta(ActionBase.Meta):
        db_table = 'movies_like'