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


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
  review = Review.objects.annotate(like_count=Count('likes')).filter(pk=review_pk).first()

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


@api_view(['GET', 'POST'])
def comment_list(request, review_pk):
  review = get_object_or_404(Review, pk=review_pk)

  if request.method == 'GET':
    comments = review.review_comments.all()  
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    print(request.data)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user, review=review)  
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_403_FORBIDDEN)
  

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, review_id=review_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Movieforyou 
@api_view(['GET', 'POST'])
def movieforyou_list(request):
  if request.method == 'GET':
    movies = Movieforyou.objects.all()
    serializer = MovieforyouSerializer(movies, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = MovieforyouSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user) 
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movieforyou_detail(request, movie_pk):
    movie = get_object_or_404(Movieforyou, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieforyouSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieforyouSerializer(movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
