from django.urls import path
from . import views


app_name = "community"
urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('best-reviews/', views.best_reviews, name='best_reviews'),
    path('reviews/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('reviews/<int:review_pk>/likes/', views.review_likes, name='review_likes'),
    path('reviews/<int:review_pk>/comments/', views.comment_list, name='comment_list'),  
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),  
    path('test-result/', views.movieforyou, name='movieforyou_result'),
    path('save-result/', views.save_result, name='save_result'),
]
