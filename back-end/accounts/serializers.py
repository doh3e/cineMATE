from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class CustomUserSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'birthday', 'profile_image', 'date_joined', 'last_login']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['nickname'] = user.nickname
        token['birthday'] = str(user.birthday) if user.birthday else None
        token['profile_image'] = user.profile_image.url if user.profile_image else None
        token['date_joined'] = str(user.date_joined) if user.date_joined else None
        token['last_login'] = str(user.last_login) if user.last_login else None
        return token