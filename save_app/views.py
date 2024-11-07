from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SavedPost
from .serializers import SavedPostSerializer
from posts_app.models import Post
from django.utils import timezone

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

    def list_saved_posts(self, request, user_id=None):
        saved_posts = SavedPost.objects.filter(user_id=user_id)
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
