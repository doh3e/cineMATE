from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.conf import settings
import requests, json

from .models import Movie, Genre
from .serializers import TopRatedMovieListSerializer, MovieDetailSerializer

# Create your views here.

@api_view(['GET'])
def load_top_rated_data(request):
  try:
    if not Movie.objects.exists():
      MOVIE_API_URL = "https://api.themoviedb.org/3/movie/top_rated"
      MOVIE_API_KEY = settings.MOVIE_API_KEY
      page = 1
      total_movies = 100  # 가져올 영화 개수
      movies_count = 0  # 현재 저장된 영화 개수

      while movies_count < total_movies:
        params = {
          'api_key': MOVIE_API_KEY,
          'language': 'ko-KR',
          'page': page
        }

        response = requests.get(MOVIE_API_URL, params=params)
        if response.status_code != 200:
          return JsonResponse({"error": "Failed to retrieve data", "status_code": response.status_code}, status=response.status_code)

        response_data = response.json()
        for item in response_data['results']:
          if movies_count >= total_movies:
            break  # 100개 이상이면 종료

          movie = Movie.objects.create(
            movie_code=item['id'],
            movie_title=item['title'],
            movie_overview=item['overview'],
            is_adult=item['adult'],
            movie_popularity=item['popularity'],
            movie_rating=item['vote_average'],
            release_date=item['release_date'],
            poster_path=item['poster_path']
          )
          
          # 영화에 장르 추가
          for genre_id in item['genre_ids']:
            try:
              genre = Genre.objects.get(pk=genre_id)
              movie.genres.add(genre)
            except Genre.DoesNotExist:
              print(f"Genre with id {genre_id} does not exist")

          movies_count += 1  # 저장된 영화 수 증가

        page += 1  # 다음 페이지로 넘어감

      return JsonResponse({"success": True, "message": "영화가 성공적으로 등록되었습니다."}, status=200)
    else:
      return JsonResponse({"success": True, "message": "영화 데이터가 이미 존재합니다."}, status=200)
  except Exception as e:
    print("서버 오류 발생:", e)
    return JsonResponse({"error": "서버 오류가 발생했습니다."}, status=500)


@api_view(['GET'])
def index(request):
    paginator = PageNumberPagination()
    paginator.page_size = 20

    movies = Movie.objects.prefetch_related('genres').all().order_by('-movie_popularity')
    result_page = paginator.paginate_queryset(movies, request)

    serializer = MovieDetailSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
