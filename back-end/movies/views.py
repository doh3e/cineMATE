from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from collections import Counter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
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
    movies = Movie.objects.prefetch_related('genre_ids').order_by('-popularity')
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data, status=200)
  except Exception as e:
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

  bookmark, created = Bookmark.objects.get_or_create(user=request.user, id=id, defaults={
    'title': movie_data.get('title'),
    'overview': movie_data.get('overview'),
    'adult': movie_data.get('adult'),
    'popularity': movie_data.get('popularity'),
    'vote_average': movie_data.get('vote_average'),
    'release_date': movie_data.get('release_date'),
    'poster_path': movie_data.get('poster_path'),
  })

  genre_ids = movie_data.get('genre_ids', [])
  if genre_ids and isinstance(genre_ids[0], dict):  # genre_ids가 딕셔너리 리스트인 경우
    genre_ids = [genre['id'] for genre in genre_ids]

  genres = Genre.objects.filter(id__in=genre_ids)

  if created:
    bookmark.genre_ids.set(genres)
    action = 'added'
  else:
    bookmark.delete()
    action = 'removed'

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


  like, created = Like.objects.get_or_create(user=request.user, id=id, defaults={
    'title': movie_data.get('title'),
    'overview': movie_data.get('overview'),
    'adult': movie_data.get('adult'),
    'popularity': movie_data.get('popularity'),
    'vote_average': movie_data.get('vote_average'),
    'release_date': movie_data.get('release_date'),
    'poster_path': movie_data.get('poster_path'),
  })

  genre_ids = movie_data.get('genre_ids', [])
  if genre_ids and isinstance(genre_ids[0], dict):  # genre_ids가 딕셔너리 리스트인 경우
    genre_ids = [genre['id'] for genre in genre_ids]
    
  genres = Genre.objects.filter(id__in=genre_ids)

  if created:
    like.genre_ids.set(genres)
    action = 'added'
  else:
    like.delete()
    action = 'removed'

  return Response({'action': action, 'movie_id': id}, status=status.HTTP_200_OK)


@api_view(['GET'])
def recommend(request, category):
  MOVIE_API_URL = 'https://api.themoviedb.org/3/discover/movie'
  user = request.user
  print(user)

  bookmarked_movie_ids = Bookmark.objects.filter(user=user).values_list('id', flat=True)
  liked_movie_ids = Like.objects.filter(user=user).values_list('id', flat=True)
  excluded_movie_ids = set(bookmarked_movie_ids).union(set(liked_movie_ids))

  if category == 'default':
    bookmark_genres = Genre.objects.filter(bookmark__user_id=user.id).values_list('id', flat=True)
    like_genres = Genre.objects.filter(like__user_id=user.id).values_list('id', flat=True)

    all_genres = list(bookmark_genres) + list(like_genres)
    genre_counts = Counter(all_genres)
    top_two_genres = [str(genre_id) for genre_id, count in genre_counts.most_common(2)]
    with_genres = ','.join(top_two_genres) if top_two_genres else None

    print(with_genres)

    params = {
      'api_key': MOVIE_API_KEY,
      'language': 'ko-KR',
      'page': 1,
      'sort_by': 'vote_average.desc',
      'include_adult': 'false',
      'vote_average.gte': 7.5,
      'vote_count.gte': 2000,
      'with_genres': with_genres,
    }

    try:
      filtered_results = []
      while len(filtered_results) < 20:
        response = requests.get(MOVIE_API_URL, params=params)
        if response.status_code != 200:
          break

        data = response.json()
        results = data.get('results', [])

        new_movies = [
          movie for movie in results
          if movie['id'] not in excluded_movie_ids
        ]

        filtered_results.extend(new_movies)

        if len(filtered_results) >= 20:
          break

        # 다음 페이지로 이동
        params['page'] += 1

        # 더 이상 데이터가 없으면 중단
        if params['page'] > data.get('total_pages', 1):
          break

      # 결과 반환
      return Response(filtered_results[:20], status=200)

    except Exception as e:
      return Response({'error': str(e)}, status=500)