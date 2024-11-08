from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import SavedPostSerializer, SavedArtistSerializer
from .models import SavedPost, SavedArtist
from posts_app.models import Post
from userprofile_app.models import Profile


class SavedArtistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, artist_id=None):
        """Save an artist profile."""
        try:
            artist_profile = Profile.objects.get(user_id=artist_id)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Artist does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_artist, created = SavedArtist.objects.get_or_create(user=user, artist_profile=artist_profile)
        if not created:
            return Response({
                "status": "error",
                "message": "Artist is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Artist saved successfully",
            "savedArtist": {
                "artistId": artist_profile.user.id,
                "savedAt": saved_artist.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, artist_id=None):
        """Unsave an artist profile."""
        saved_artist = SavedArtist.objects.filter(user=request.user, artist_profile__user_id=artist_id).first()
        if saved_artist:
            saved_artist.delete()
            return Response({
                "status": "success",
                "message": "Artist unsaved successfully",
                "unsavedArtist": {
                    "artistId": artist_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Artist not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_artists(self, request):
        """List all saved artist profiles for the user."""
        saved_artists = SavedArtist.objects.filter(user=request.user)
        if not saved_artists.exists():
            return Response({
                "status": "error",
                "message": "No saved artists found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SavedArtistSerializer(saved_artists, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalArtists": saved_artists.count(),
                "artists": serializer.data
            }
        }, status=status.HTTP_200_OK)

class SavedPostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, post_id=None):
        if not Post.objects.filter(id=post_id).exists():
            return Response({
                "status": "error",
                "message": "Post does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        saved_post, created = SavedPost.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            return Response({
                "status": "error",
                "message": "Post is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status": "success",
            "message": "Post saved successfully",
            "savedPost": {
                "postId": saved_post.post.id,
                "savedAt": saved_post.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, post_id=None):
        saved_post = SavedPost.objects.filter(user=request.user, post_id=post_id).first()
        if saved_post:
            saved_post.delete()
            return Response({
                "status": "success",
                "message": "Post unsaved successfully",
                "unsavedPost": {
                    "postId": post_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Post not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_posts(self, request):
        saved_posts = SavedPost.objects.filter(user=request.user)
        if not saved_posts.exists():
            return Response({
                "status": "error",
                "message": "No saved posts found for this user."
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = SavedPostSerializer(saved_posts, many=True)
        return Response({
            "status": "success",
            "savedPosts": serializer.data
        }, status=status.HTTP_200_OK)
