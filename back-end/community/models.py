from django.db import models
from django.conf import settings
from movies.models import Genre


# Create your models here.
class Review(models.Model):
    # 영화 API에서 받아올때 API 필드랑 이름이 일치하지 않으면 아주 귀찮아집니다..
    # 그래서 review의 기본키 아이디도 이름 변경함
    review_id = models.AutoField(primary_key=True)
    review_title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE)
    id = models.IntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField()
    adult = models.BooleanField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    genre_ids = models.ManyToManyField(Genre)
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    review_content = models.TextField(null=True, blank=True)
    user_rating = models.IntegerField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_likes_review')
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
    
    