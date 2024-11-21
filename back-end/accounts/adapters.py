from allauth.account.adapter import DefaultAccountAdapter
from .models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.nickname = request.data.get('nickname', '')
        user.birthday = request.data.get('birthday', None)
        user.profile_image = request.data.get('profile_image', None)
        if commit:
            user.save()
        return user
    
