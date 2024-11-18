# Generated by Django 4.2.16 on 2024-11-17 23:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(related_name='user_likes_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
