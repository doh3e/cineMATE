from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'birthday', 'profile_image', 'date_joined', 'last_login']
