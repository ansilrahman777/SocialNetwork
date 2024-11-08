from rest_framework import serializers
from .models import SavedArtist, SavedPost
from posts_app.models import Post
from userprofile_app.models import Profile
        
class ArtistProfileSerializer(serializers.ModelSerializer):
    artist_id = serializers.CharField(source='user.id', read_only=True)
    artist_name = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField() 
    # role = serializers.CharField(source='selected_role.role_name', read_only=True)
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['artist_id', 'artist_name', 'profile_image', 'cover_image']

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

class SavedArtistSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    artist_details = ArtistProfileSerializer(source='artist_profile', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedArtist
        fields = ['saved_id', 'artist_details', 'saved_at']

class PostSerializer(serializers.ModelSerializer):
    user = ArtistProfileSerializer(source='user.profile', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    post_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'caption', 'location', 'media', 'created_at', 'likes_count', 'comments_count']
        read_only_fields = ['user', 'created_at']



class SavedPostSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    post_details = PostSerializer(source='post', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedPost
        fields = ['saved_id', 'post_details', 'saved_at']

    def validate_post_id(self, value):
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("Post does not exist.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = validated_data['post_id']
        saved_post, created = SavedPost.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            raise serializers.ValidationError("Post is already saved.")
        return saved_post
