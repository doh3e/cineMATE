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

# 인기 영화 2000개 호출 (DB에 저장할 데이터)
@api_view(['GET'])
def load_top_rated_data(request):
  try:
    if not Movie.objects.exists():
      MOVIE_API_URL = "https://api.themoviedb.org/3/movie/top_rated"
      page = 1
      total_movies = 2000
      movies_count = 0

      while movies_count < total_movies:
        params = {
          'api_key': MOVIE_API_KEY,
          'language': 'ko-KR',
          'page': page
        }

        response = requests.get(MOVIE_API_URL, params=params)
        if response.status_code != 200:
          return JsonResponse({"error": "API로부터 데이터를 받아오는 데 실패했습니다.", "status_code": response.status_code}, status=response.status_code)

        response_data = response.json()
        results = response_data.get('results', [])

        if not results:
          break

        for item in results:
          if item['vote_count'] < 1000:
            continue
          if movies_count >= total_movies:
            break

          movie = Movie.objects.create(
            id=item['id'],
            title=item['title'],
            overview=item['overview'],
            adult=item['adult'],
            popularity=item['popularity'],
            vote_average=item['vote_average'],
            vote_count=item['vote_count'],
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


# 메인페이지 : top100 영화가 노출됨
@api_view(['GET'])
def index(request):
  try:
    movies = Movie.objects.prefetch_related('genre_ids').order_by('-vote_average', '-vote_count')[:100]
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data, status=200)
  except Movie.DoesNotExist:
    return Response({"error": "영화를 찾을 수 없습니다."}, status=404)
  except Exception as e:
    print(f"Unexpected error in index: {str(e)}")
    return Response({"error": "서버 오류가 발생했습니다."}, status=500)


# 영화를 검색하는 로직
@api_view(['GET'])
def movie_search(request):
  query = request.GET.get('query', '').strip()
  if not query:
    return Response({"error": "검색어를 입력해주세요."}, status=400)

  try:
    MOVIE_API_URL = "https://api.themoviedb.org/3/search/movie"
    movies = []
    page = 1
    max_results = 100
    total_results = 0

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
    
    if not movies:
      return Response({"message": "검색 결과가 없습니다."}, status=404)

    sorted_movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)

    return Response(sorted_movies, status=200)  # 최대 100개 반환
  except requests.RequestException as e:
    return Response({"error": f"TMDB API 요청 실패: {str(e)}"}, status=500)
  except Exception as e:
    return Response({"error": "서버 오류가 발생했습니다.", "details": str(e)}, status=500)


# 영화 북마크 하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark(request):
  try:
    movie_data = request.data.get('movie')
    if not movie_data:
      return Response({'error': '영화 데이터를 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    id = movie_data.get('id')
    if not id:
      return Response({'error': '영화 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

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
  except Genre.DoesNotExist as e:
    return Response({'error': f'장르 ID를 찾을 수 없습니다: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    return Response({'error': f'서버 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 영화 좋아요 하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request):
  try:
    movie_data = request.data.get('movie')
    if not movie_data:
      return Response({'error': '영화 데이터를 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    id = movie_data.get('id')
    if not id:
      return Response({'error': '영화 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)


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
    if genre_ids and isinstance(genre_ids[0], dict):
      genre_ids = [genre['id'] for genre in genre_ids]
      
    genres = Genre.objects.filter(id__in=genre_ids)

    if created:
      like.genre_ids.set(genres)
      action = 'added'
    else:
      like.delete()
      action = 'removed'

    return Response({'action': action, 'movie_id': id}, status=status.HTTP_200_OK)
  
  except Genre.DoesNotExist as e:
    return Response({'error': f'장르 ID를 찾을 수 없습니다: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    return Response({'error': f'서버 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 조건에 따른 추천 영화 (분기: 기본(선호기반) / 유사도기반 / 생일 / 특별한 날 )
@api_view(['GET'])
def recommend(request, category):
  MOVIE_API_URL = 'https://api.themoviedb.org/3/discover/movie'
  user = request.user

  bookmarked_movie_ids = Bookmark.objects.filter(user=user).values_list('id', flat=True)
  liked_movie_ids = Like.objects.filter(user=user).values_list('id', flat=True)
  excluded_movie_ids = set(bookmarked_movie_ids).union(set(liked_movie_ids))

  params = {}
  
  # 기본 추천
  if category == 'default':
    bookmark_genres = Genre.objects.filter(bookmark__user_id=user.id).values_list('id', flat=True)
    like_genres = Genre.objects.filter(like__user_id=user.id).values_list('id', flat=True)

    all_genres = list(bookmark_genres) + list(like_genres)
    genre_counts = Counter(all_genres)
    top_two_genres = [str(genre_id) for genre_id, count in genre_counts.most_common(2)]
    with_genres = ','.join(top_two_genres) if top_two_genres else None

    params = {
      'api_key': MOVIE_API_KEY,
      'language': 'ko-KR',
      'page': 1,
      'sort_by': 'vote_count.desc',
      'include_adult': 'false',
      'vote_average.gte': 7.0,
      'vote_count.gte': 1000,
      'with_genres': with_genres,
    }

  # 유저 유사도 기반 추천
  if category == 'similarity':

    similar_users = (
      Like.objects.filter(id__in=excluded_movie_ids)
      .exclude(user=user)
      .values('user')
      .annotate(common_movies=Count('id'))
      .order_by('-common_movies')
    )

    similar_user_ids = [entry['user'] for entry in similar_users[:3]]

    similar_movies = Movie.objects.filter(
        id__in=Like.objects.filter(user__in=similar_user_ids)
        .exclude(id__in=excluded_movie_ids)
        .values_list('id', flat=True)
    )

    sorted_movies = similar_movies.order_by('-vote_average', '-popularity')[:20]

    serialized_movies = [
      {
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'adult': movie.adult,
        'poster_path': movie.poster_path,
        'vote_average': movie.vote_average,
        'vote_count': movie.vote_count,
        'popularity': movie.popularity,
        'genre_ids': list(movie.genre_ids.values_list('id', flat=True)),
        'release_date': movie.release_date,
      }
      for movie in sorted_movies
    ]

    return Response(serialized_movies, status=200)
  
  # 생일인 사람
  if category == 'birthday':
    if not hasattr(user, 'birthday') or not user.birthday:
      return Response({'error': '생년월일 정보가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    params = {
      'api_key': MOVIE_API_KEY,
      'language': 'ko-KR',
      'page': 1,
      'sort_by': 'vote_average.desc',
      'include_adult': 'false',
      'vote_average.gte': 7.0,
      'vote_count.gte': 1000,
      'primary_release_year': user.birthday.year,
    }
  
  if category == 'eventday':
    keyword = request.GET.get('keyword', '').strip()
    if not keyword:
      return Response({'error': '키워드를 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    origin = ''
    if keyword == '설날' or keyword == '추석':
      genre = '10751,35' # 가족, 코미디
    elif keyword == '어린이날':
      genre = '10751,16' # 가족, 애니메이션
    elif keyword == '할로윈':
      genre = '27' # 공포
    elif keyword == '어버이날':
      genre = '10751' # 가족
      filter_word = ['엄마', '아빠', '어머니', '아버지']
    elif keyword == '크리스마스 이브' or keyword == '크리스마스':
      genre = '10749' # 로맨스
      filter_word = ['크리스마스', '성탄절', '12월 25일', '산타']
    elif keyword == '새해' or keyword == '연말':
      genre = '18|35|10751|12|14' # 드라마, 코미디, 가족, 모험, 판타지
      filter_word = ['새해', '1월 1일', '연말', '신년', '12월 31일', 'new year']
    elif keyword == '발렌타인데이' or keyword == '화이트데이':
      genre = '10749' # 로맨스
      filter_word = ['초콜릿', '발렌타인', '화이트데이', '연인']
    elif keyword == '광복절' or keyword == '삼일절':
      genre = '36' # 역사
      origin = 'ko'
      filter_word = ['일본', '일제강점기', '1945년', '3월 1일', '삼일절',
                     '일제 치하', '1910년', '1920년', '1930년', '광복']
    elif keyword == '프로젝트 발표연습' or keyword == '프로젝트 발표날':
      genre = '9648'
      filter_word = ['발표', '프레젠테이션', '코딩', '개발자', '공부', '두뇌', '천재', '컴퓨터', '해커']
      
    params = {
      'api_key': MOVIE_API_KEY,
      'language': 'ko-KR',
      'page': 1,
      'sort_by': 'vote_count.desc',
      'include_adult': 'false',
      'vote_average.gte': 7,
      'vote_count.gte': 100,
      'with_genres': genre,
      'with_original_language': origin,
    }
    
  try:
    filtered_results = []
    while len(filtered_results) < 20:
      response = requests.get(MOVIE_API_URL, params=params)
      if response.status_code != 200:
        break

      data = response.json()
      results = data.get('results', [])

      new_movies = []
      for movie in results:
        if movie['id'] in excluded_movie_ids:
          continue

        if 'filter_word' in locals():
          title = movie.get('title', '')
          overview = movie.get('overview', '')

          if not any(word in title or word in overview for word in filter_word):
            continue

        new_movies.append(movie)

      filtered_results.extend(new_movies)

      if len(filtered_results) >= 20:
        break

      params['page'] += 1

      if params['page'] > data.get('total_pages', 1):
        break

    return Response(filtered_results[:20], status=200)

  except requests.RequestException as e:
    return Response({'error': f'TMDB API 호출 실패: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    return Response({'error': f'서버 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def moviebygenre(request, genre_id):
  movies = Movie.objects.filter(genre_ids__id=genre_id)
  serializer = MovieDetailSerializer(movies, many=True)
  return Response(serializer.data)
    