from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'user_{0}/{1}'.format(instance.username, filename)

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    birthday = models.DateField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')