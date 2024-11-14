from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50)
    

class Movie(models.Model):
    movie_code = models.IntegerField()
    movie_title = models.CharField(max_length=200)
    movie_overview = models.TextField()
    is_adult = models.BooleanField()
    movie_popularity = models.FloatField()
    movie_rating = models.FloatField() # vote_average
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_movies')

