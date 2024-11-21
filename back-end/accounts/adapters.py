from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.utils.timezone import now
from .models import User


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.nickname = form.cleaned_data.get('nickname', '')  # POST 데이터를 form에서 가져옴
        user.birthday = form.cleaned_data.get('birthday', None)
        user.profile_image = form.cleaned_data.get('profile_image', None)
        if commit:
            user.save()
        return user


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'user_{0}/{1}'.format(instance.username, filename)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 카카오 사용자 정보 가져오기
        kakao_account = sociallogin.account.extra_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})

        # 이메일 설정
        if kakao_account.get('email'):
            user.email = kakao_account['email']

        # 닉네임 설정
        user.nickname = profile.get('nickname', f"kakao_{sociallogin.account.uid}")

        # 유니크한 username 생성
        user.username = kakao_account.get('email', f"kakao_{sociallogin.account.uid}").split('@')[0]
        if User.objects.filter(username=user.username).exists():
            user.username += f"_{uuid4().hex[:5]}"

        # 프로필 이미지 저장
        profile_image_url = profile.get('profile_image_url')
        if profile_image_url:
            response = requests.get(profile_image_url)
            if response.status_code == 200:
                file_name = user_directory_path(user, profile_image_url.split('/')[-1])
                user.profile_image.save(file_name, ContentFile(response.content), save=False)

        # 생년월일 설정
        user.birthday = kakao_account.get('birthday', None)

        return user