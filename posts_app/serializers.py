from rest_framework import serializers
from .models import Headshot, Post, Like, Comment
from userprofile_app.models import Profile
from .backblaze_custom_storage import CustomBackblazeStorage, custom_upload_to


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    profile_image = serializers.URLField()

    class Meta:
        model = Profile
        fields = ['username', 'profile_image']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'location', 'media', 'media_type', 'created_at', 'likes_count', 'comments_count']
        read_only_fields = ['user', 'media_type', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class HeadshotSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Headshot
        fields = ['id', 'user', 'banner', 'film_name', 'role_played', 'created_at']