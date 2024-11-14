from rest_framework import serializers
from .models import Review, Comment, Movieforyou

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  
        read_only_fields = ('user', 'created_at', 'updated_at')  

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at') 

class MovieforyouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movieforyou
        fields = '__all__'
        read_only_fields = ('user',) 


