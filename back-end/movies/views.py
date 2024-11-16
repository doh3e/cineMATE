from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests, json

from .models import Movie, Genre, Bookmark, Like
from .serializers import MovieDetailSerializer

# Create your views here.

MOVIE_API_KEY = settings.MOVIE_API_KEY

@api_view(['GET'])
def load_top_rated_data(request):
  try:
    if not Movie.objects.exists():
      MOVIE_API_URL = "https://api.themoviedb.org/3/movie/top_rated"
      page = 1
      total_movies = 100
      movies_count = 0

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
        results = response_data.get('results', [])

        if not results:
          break

        for item in results:
          if movies_count >= total_movies:
            break

          movie = Movie.objects.create(
            id=item['id'],
            title=item['title'],
            overview=item['overview'],
            adult=item['adult'],
            popularity=item['popularity'],
            vote_average=item['vote_average'],
            release_date=item['release_date'],
            poster_path=item['poster_path']
          )

          for genre_id in item['genre_ids']:
            try:
              genre = Genre.objects.get(pk=genre_id)
              movie.genre_ids.add(genre)
            except Genre.DoesNotExist:
              print(f"Genre with id {genre_id} does not exist")

          movies_count += 1

        page += 1

        if page > response_data.get('total_pages', 1):
          break

      return JsonResponse({"success": True, "message": "영화가 성공적으로 등록되었습니다."}, status=200)
    else:
      return JsonResponse({"success": True, "message": "영화 데이터가 이미 존재합니다."}, status=200)
  except Exception as e:
    print("서버 오류 발생:", e)
    return JsonResponse({"error": "서버 오류가 발생했습니다."}, status=500)


@api_view(['GET'])
def index(request):
  try:
    movies = Movie.objects.annotate(
      bookmarks_count=Count('bookmark'),
      likes_count=Count('like')
    ).prefetch_related('genre_ids').order_by('-popularity')

    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data, status=200)
  except Exception as e:
    # 에러 처리
    return Response({"error": str(e)}, status=500)



@api_view(['GET'])
def movie_search(request):
  query = request.GET.get('query', '').strip()
  if not query:
    return Response({"error": "검색어를 입력해주세요."}, status=400)

  try:
    MOVIE_API_URL = "https://api.themoviedb.org/3/search/movie"
    movies = []  # 결과 저장 리스트
    page = 1
    max_results = 100  # 최대 100개
    total_results = 0  # 가져온 영화 개수

    while total_results < max_results:
      params = {
        'api_key': MOVIE_API_KEY,
        'language': 'ko-KR',
        'query': query,
        'page': page,
      }

      response = requests.get(MOVIE_API_URL, params=params)
      if response.status_code != 200:
        return Response({"error": "TMDB API 호출 실패"}, status=response.status_code)

      response_data = response.json()
      results = response_data.get('results', [])
      if not results:
        break

      movies.extend(results[:max_results - total_results])
      total_results = len(movies)
      page += 1

      if page > response_data.get('total_pages', 1):
        break

    sorted_movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)

    return Response(sorted_movies)  # 최대 100개 반환
  except Exception as e:
    return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark(request):
    movie_data = request.data.get('movie')
    if not movie_data:
        return Response({'error': 'movie data is required'}, status=status.HTTP_400_BAD_REQUEST)

    id = movie_data.get('id')
    if not id:
        return Response({'error': 'movie_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    movie, _ = Movie.objects.get_or_create(
        id=id,
        defaults={
            'title': movie_data['title'],
            'overview': movie_data['overview'],
            'adult': movie_data['adult'],
            'popularity': movie_data['popularity'],
            'vote_average': movie_data['vote_average'],
            'release_date': movie_data['release_date'],
            'poster_path': movie_data['poster_path'],
        }
    )

    bookmark, created = Bookmark.objects.get_or_create(user=request.user, id=movie.id, defaults={
        'title': movie.title,
        'overview': movie.overview,
        'adult': movie.adult,
        'popularity': movie.popularity,
        'vote_average': movie.vote_average,
        'release_date': movie.release_date,
        'poster_path': movie.poster_path,
    })

    if not created:
        bookmark.delete()
        action = 'removed'
    else:
        action = 'added'

    return Response({'action': action, 'movie_id': id}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request):
    movie_data = request.data.get('movie')
    if not movie_data:
        return Response({'error': 'movie data is required'}, status=status.HTTP_400_BAD_REQUEST)

    id = movie_data.get('id')
    if not id:
        return Response({'error': 'movie_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    movie, _ = Movie.objects.get_or_create(
        id=id,
        defaults={
            'title': movie_data['title'],
            'overview': movie_data['overview'],
            'adult': movie_data['adult'],
            'popularity': movie_data['popularity'],
            'vote_average': movie_data['vote_average'],
            'release_date': movie_data['release_date'],
            'poster_path': movie_data['poster_path'],
        }
    )

    like, created = Like.objects.get_or_create(user=request.user, id=movie.id, defaults={
        'title': movie.title,
        'overview': movie.overview,
        'adult': movie.adult,
        'popularity': movie.popularity,
        'vote_average': movie.vote_average,
        'release_date': movie.release_date,
        'poster_path': movie.poster_path,
    })

    if not created:
        like.delete()
        action = 'removed'
    else:
        action = 'added'

    return Response({'action': action, 'movie_id': id}, status=status.HTTP_200_OK)