from django.urls import path
from . import views


app_name = "movies"
urlpatterns = [
    path('', views.index),
    path('load-top-list/', views.load_top_rated_data),
    path('search/', views.movie_search),
    path('bookmark/', views.bookmark),
    path('like/', views.like),
    path('recommend/<str:category>/', views.recommend),
    path('movie-by-genre/<int:genre_id>/', views.moviebygenre),
    path('get-movie-reviews/<int:movie_id>/', views.get_reviews),
    path('get-movie-stats/<int:movie_id>/', views.get_movie_stats),
]