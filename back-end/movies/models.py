from django.db import models
from django.conf import settings


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
  pk_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )
  id = models.IntegerField()
  title = models.CharField(max_length=200)
  overview = models.TextField()
  adult = models.BooleanField()
  popularity = models.FloatField()
  vote_average = models.FloatField()
  genre_ids = models.ManyToManyField(Genre)
  release_date = models.DateField()
  poster_path = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    abstract = True



class Bookmark(ActionBase):
  class Meta(ActionBase.Meta):
    db_table = 'movies_bookmark'
    constraints = [
      models.UniqueConstraint(fields=['user', 'id'], name='unique_user_movie_bookmark')
    ]


class Like(ActionBase):
  class Meta(ActionBase.Meta):
    db_table = 'movies_like'
    constraints = [
      models.UniqueConstraint(fields=['user', 'id'], name='unique_user_movie_like')
    ]
