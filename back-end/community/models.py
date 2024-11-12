from django.db import models
from django.conf import settings
from movies.models import Genre


# Create your models here.
class Review(models.Model):
    review_title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE)
    review_movie = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)
    is_adult = models.BooleanField()
    overview = models.TextField(null=True, blank=True)
    movie_rating = models.FloatField()
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    release_date = models.DateField()
    review_content = models.TextField(null=True, blank=True)
    user_rating = models.IntegerField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comments', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='review_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Movieforyou(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_friendcards', on_delete=models.CASCADE)
    friend_name = models.CharField(max_length=100)
    movie_code = models.IntegerField()
    movie_title = models.CharField(max_length=100)
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    card_img = models.CharField(max_length=200)
    
    