from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

def signup(request):
    pass


def login(request):
    pass


def logout(request):
    pass