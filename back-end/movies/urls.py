from django.urls import path
from . import views


app_name = "movies"
urlpatterns = [
    path('', views.index),
    path('load-top-list/', views.load_top_rated_data),
]