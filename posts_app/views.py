from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Headshot, Post, Like, Comment
from .serializers import HeadshotSerializer, PostSerializer, LikeSerializer, CommentSerializer
from userprofile_app.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model() 

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response({
                "status": "success",
                "message": "Post created successfully",
                "data": PostSerializer(post).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Failed to create post",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list_images(self, request, user_id=None):
        try:
            user = get_object_or_404(User, pk=user_id)
            images = Post.objects.filter(media_type='image', user=user)
            if not images.exists():
                return Response({
                    "status": "error",
                    "message": "No images found for this user."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(images, many=True)
            return Response({
                "status": "success",
                "message": "Images retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "An error occurred while retrieving images.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_videos(self, request, user_id=None):
        try:
            user = get_object_or_404(User, pk=user_id)
            videos = Post.objects.filter(media_type='video', user=user)
            if not videos.exists():
                return Response({
                    "status": "error",
                    "message": "No videos found for this user."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(videos, many=True)
            return Response({
                "status": "success",
                "message": "Videos retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "An error occurred while retrieving videos.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        data['post'] = pk  
        serializer = CommentSerializer(data=data, context={'request': request})
               
        if serializer.is_valid():
            comment = serializer.save(user=request.user, post=Post.objects.get(id=pk))
            return Response({
                "status": "success",
                "message": "Comment added successfully",
                "data": CommentSerializer(comment).data
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

    def list_comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": "success",
            "message": "Comments retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def list_likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response({
            "status": "success",
            "message": "Likes retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        View to retrieve details of a single post.
        """
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({
            "status": "success",
            "message": "Post details retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def share(self, request, pk=None):
        """
        View to generate a shareable link for a specific post.
        """
        post = get_object_or_404(Post, pk=pk)
        username = post.user.username  # Assuming Post model has a user relationship
        # Generate the link to the post detail view
        share_link = f"{request.build_absolute_uri(reverse('post-detail', args=[pk]))}?user={username}"
        return Response({
            "status": "success",
            "message": "Share link generated",
            "share_link": share_link
        }, status=status.HTTP_200_OK)
        
class HeadshotViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        
        banner = request.FILES.get('banner')
        if banner and not banner.content_type.startswith('image/'):
            return Response({
                "status": "error",
                "message": "Invalid file type. Only images are allowed for banners."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HeadshotSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            headshot = serializer.save(user=request.user)
            return Response({
                "status": "success",
                "message": "Headshot created successfully.",
                "data": HeadshotSerializer(headshot).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Failed to create headshot.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            headshot = get_object_or_404(Headshot, pk=pk)
            serializer = HeadshotSerializer(headshot)
            return Response({
                "status": "success",
                "message": "Headshot retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Headshot.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Headshot not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def list_user_headshots(self, request, user_id=None):
        headshots = Headshot.objects.filter(user__id=user_id)
        
        if not headshots.exists():
            return Response({
                "status": "error",
                "message": "No headshots found for this user."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HeadshotSerializer(headshots, many=True)
        return Response({
            "status": "success",
            "message": "User headshots retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
