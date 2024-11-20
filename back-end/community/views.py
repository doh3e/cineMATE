from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Review, Comment, Movieforyou
from .serializers import ReviewSerializer, ListReviewSerializer, ReviewDetailSerializer
from .serializers import CommentSerializer, MovieforyouSerializer
from django.db.models import Count
from django.conf import settings
import requests, json

from movies.models import Genre

MOVIE_API_KEY = settings.MOVIE_API_KEY

# 리뷰 목록을 호출
@api_view(['GET', 'POST'])
def review_list(request):
  if request.method == 'GET':
    reviews = Review.objects.annotate(
    like_count=Count('likes'),
    comment_count=Count('review_comments')
    ).order_by('-created_at')
    
    page_size = 3
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size

    paginated_reviews = reviews[start:end]

    total_reviews = reviews.count()
    total_pages = (total_reviews + page_size - 1) // page_size

    serializer = ListReviewSerializer(paginated_reviews, many=True)
    
    return Response({
      'count': total_reviews,
      'total_pages': total_pages,
      'current_page': page,
      'results': serializer.data
    })

  elif request.method == 'POST':
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰의 디테일 페이지를 보는 요청
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
  try:
    review = Review.objects.annotate(like_count=Count('likes')).filter(pk=review_pk).first()
    if not review:
      return Response({'error': '리뷰를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
      serializer = ReviewDetailSerializer(review)
      return Response(serializer.data)

    elif request.method == 'PUT':
      serializer = ReviewDetailSerializer(review, data=request.data, partial=True)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
      if review.user_id != request.user.id:
        return Response({'detail': '삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
      review.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

  except Exception as e:
    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

# 리뷰에 좋아요 누르기
@api_view(['POST'])
def review_likes(request, review_pk):
  review = get_object_or_404(Review, pk=review_pk)
  user = request.user
  if review.likes.filter(id=user.id).exists():
    review.likes.remove(user)
    message = "unliked"
  else:
    review.likes.add(user)
    message = "liked"

  return Response({
    'message': message,
    'like_count': review.likes.count(),
    'liked_users': list(review.likes.values_list('id', flat=True))
  }, status=status.HTTP_200_OK)   


# 댓글 목록, 댓글 생성
@api_view(['GET', 'POST'])
def comment_list(request, review_pk):
  try:
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
      comments = review.review_comments.all()
      serializer = CommentSerializer(comments, many=True)
      return Response(serializer.data)

    elif request.method == 'POST':
      serializer = CommentSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  except Exception as e:
    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

# 댓글 상세(수정 삭제)
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, review_pk, comment_pk):
  try:
    comment = get_object_or_404(Comment, pk=comment_pk, review_id=review_pk)

    if request.method == 'GET':
      serializer = CommentSerializer(comment)
      return Response(serializer.data)

    elif request.method == 'DELETE':
      if comment.user_id != request.user.id:
        return Response({'error': '삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

  except Exception as e:
    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 무비포유
# GET : 지인에게 어울리는 영화를 API와 자체 로직을 통해 제공해줌
# POST 만들어진 무비포유를 저장
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def movieforyou(request):
  MOVIE_API_URL = 'https://api.themoviedb.org/3/discover/movie'
  user = request.user
  friend_name = request.GET.get('friendName')
  top_genre = request.GET.get('topGenre')
  birth_month = request.GET.get('birthMonth')
  final_message = request.GET.get('finalMessage')
  preference = request.GET.get('preference')
  
  if not top_genre:
    return Response({'error': '장르 정보를 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

  genre = get_object_or_404(Genre, name=top_genre)
  genre_id = genre.id
  
  if birth_month and len(birth_month) == 1:
    birth_month = birth_month.zfill(2)
    
  if request.method == 'GET':
    if preference == '평범':
      params = {
        'api_key': MOVIE_API_KEY,
        'language': 'ko-KR',
        'page': 1,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'with_genres': genre_id,
        'vote_average.gte': 7.0,
        'vote_average.lte': 8.0,
        'vote_count.gte': 2000,
      }
    elif preference == '다좋아':
      params = {
        'api_key': MOVIE_API_KEY,
        'language': 'ko-KR',
        'page': 1,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'with_genres': genre_id,
        'vote_average.gte': 7.5,
        'vote_count.gte': 3000,
      }
    elif preference == '홍대병':
      params = {
        'api_key': MOVIE_API_KEY,
        'language': 'ko-KR',
        'page': 1,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'with_genres': genre_id,
        'vote_average.gte': 8.0,
        'vote_count.gte': 1000,
      }     

  elif request.method == 'POST':
    pass
  
  try:
    filtered_results = []
    while len(filtered_results) < 20:
      response = requests.get(MOVIE_API_URL, params=params)
      if response.status_code != 200:
        return Response({'error': 'TMDB API 호출 실패'}, status=response.status_code)
  
      data = response.json()
      results = data.get('results', [])
      
      for movie in results:
        if movie['release_date'][5:7] == birth_month:
          filtered_results.append(movie)
      
      if len(filtered_results) >= 20:
        break
      params['page'] += 1

      if params['page'] > data.get('total_pages', 1):
        break
    
    print(filtered_results)
    result_movie = filtered_results[0] if filtered_results else None
    
    return Response({
      'movie': result_movie,
      'my_choice': {
        'friend_name': friend_name,
        'top_genre': top_genre,
        'birth_month': birth_month,
        'final_message': final_message,
        'preference': preference,
      }
    })
    
  except Genre.DoesNotExist:
    return Response({'error': '해당 장르를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
  except requests.RequestException as e:
    return Response({'error': f'TMDB API 요청 실패: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)