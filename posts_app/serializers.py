from rest_framework import serializers
from .models import Headshot, Post, Like, Comment
from userprofile_app.models import Profile


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
    post_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'caption', 'location', 'media', 'media_type', 'created_at', 'likes_count', 'comments_count']
        read_only_fields = ['user', 'media_type', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)
    like_id = serializers.IntegerField(source='id', read_only=True) 

    class Meta:
        model = Like
        fields = ['like_id', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)
    comment_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'content', 'created_at']

class HeadshotSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='user.profile', read_only=True)
    headshot_id = serializers.IntegerField(source='id', read_only=True)  

    class Meta:
        model = Headshot
        fields = ['headshot_id', 'user', 'banner', 'film_name', 'role_played', 'created_at']