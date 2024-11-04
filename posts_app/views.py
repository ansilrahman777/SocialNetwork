from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Post created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Failed to create post",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list_images(self, request):
        images = Post.objects.filter(media_type='image')
        serializer = PostSerializer(images, many=True)
        return Response({
            "status": "success",
            "message": "Images retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def list_videos(self, request):
        videos = Post.objects.filter(media_type='video')
        serializer = PostSerializer(videos, many=True)
        return Response({
            "status": "success",
            "message": "Videos retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({
                "status": "error",
                "message": "Already liked"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": "success",
            "message": "Post liked"
        }, status=status.HTTP_201_CREATED)

    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({
            "status": "success",
            "message": "Post unliked"
        }, status=status.HTTP_200_OK)

    def comment(self, request, pk=None):
        data = request.data.copy()
        data['user'] = request.user.id
        data['post'] = pk
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Comment added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Failed to add comment",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete_comment(self, request, pk=None, comment_id=None):
        comment = get_object_or_404(Comment, pk=comment_id, post__id=pk, user=request.user)
        comment.delete()
        return Response({
            "status": "success",
            "message": "Comment deleted"
        }, status=status.HTTP_200_OK)

    def share(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        share_link = request.build_absolute_uri(reverse('post-detail', args=[pk]))
        return Response({
            "status": "success",
            "message": "Share link generated",
            "share_link": share_link
        }, status=status.HTTP_200_OK)

    def list_comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": "success",
            "message": "Comments retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def list_likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response({
            "status": "success",
            "message": "Likes retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
