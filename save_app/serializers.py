from rest_framework import serializers
from .models import SavedApprenticeship, SavedArtist, SavedEvent, SavedInternship, SavedProject, SavedCastingCall, SavedGigWork, SavedPost
from posts_app.models import Post
from userprofile_app.models import Profile
from forms.models import Project, GigWork, CastingCall, EventDetails, Internship, Apprenticeship
        
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


class ProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Project
        fields = [
            'user_id', 'username', 'project_title', 'project_tagline', 'film_name', 
            'film_role', 'project_status', 'progress_percentage', 'project_type', 'language', 
            'description', 'primary_email', 'secondary_email', 'team_name', 'artist_name', 
            'role', 'image_files', 'video_files', 'hashtags', 'press_release_link', 
            'media_release_link', 'social_media_links', 'genre', 'created_at'
        ]
        read_only_fields = ['user_id', 'username', 'created_at']

class SavedProjectSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    project_details = ProjectSerializer(source='project', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedProject
        fields = ['saved_id', 'project_details', 'saved_at']


class GigWorkSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = GigWork
        fields = [
            'user_id', 'username', 'work_type', 'project_id', 'gig_title', 'short_description', 
            'work_hours', 'hours_type', 'price', 'price_type', 'skills', 'progress_of_project',
            'work_method', 'promotion', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'username', 'created_at', 'updated_at']

class SavedGigWorkSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    gig_details = GigWorkSerializer(source='gig_work', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedGigWork
        fields = ['saved_id', 'gig_details', 'saved_at']


class CastingCallSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CastingCall
        fields = [
            'user_id', 'username', 'job_title', 'project_link', 'short_description', 
            'gender', 'experience', 'role_type', 'age', 'skills', 'height', 'body_type', 
            'script_file', 'script_url', 'audition_type', 'offline_location', 
            'casting_call_date', 'casting_call_end_date', 'start_time', 'end_time', 
            'created_at'
        ]
        read_only_fields = ['user_id', 'username', 'created_at']

class SavedCastingCallSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    casting_call_details = CastingCallSerializer(source='casting_call', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedCastingCall
        fields = ['saved_id', 'casting_call_details', 'saved_at']
        

class EventDetailsSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = EventDetails
        fields = ['event_id', 'event_title', 'event_location', 'event_date', 'event_time', 'event_type', 'event_price']

class SavedEventSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    event_details = EventDetailsSerializer(source='event', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedEvent
        fields = ['saved_id', 'event_details', 'saved_at']
        


class InternshipSerializer(serializers.ModelSerializer):
    internship_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Internship
        fields = ['internship_id', 'internship_title', 'organisation_name', 'internship_type', 'type_of_work', 'start_date', 'end_date', 'duration']

class SavedInternshipSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    internship_details = InternshipSerializer(source='internship', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedInternship
        fields = ['saved_id', 'internship_details', 'saved_at']
        
        
class ApprenticeshipSerializer(serializers.ModelSerializer):
    apprenticeship_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Apprenticeship
        fields = ['apprenticeship_id', 'apprenticeship_title', 'organisation_name', 'apprenticeship_type', 'type_of_work', 'start_date', 'end_date', 'duration']

class SavedApprenticeshipSerializer(serializers.ModelSerializer):
    saved_id = serializers.IntegerField(source='id', read_only=True)
    apprenticeship_details = ApprenticeshipSerializer(source='apprenticeship', read_only=True)
    saved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SavedApprenticeship
        fields = ['saved_id', 'apprenticeship_details', 'saved_at']