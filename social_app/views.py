from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Follow, FollowRequest, Block
from .serializers import FollowSerializer, FollowRequestSerializer, BlockSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowViewSet(viewsets.ViewSet):
    def follow(self, request, user_id=None):
        follower = request.user
        if not follower.is_authenticated or follower.id == user_id:
            return Response({"error": "Invalid follow request"}, status=status.HTTP_400_BAD_REQUEST)

        following = User.objects.filter(id=user_id).first()
        if not following:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        if not created:
            return Response({"status": "Already following"}, status=status.HTTP_200_OK)

        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unfollow(self, request, user_id=None):
        follow = Follow.objects.filter(follower=request.user, following_id=user_id).first()
        if not follow:
            return Response({"error": "Not following user"}, status=status.HTTP_404_NOT_FOUND)
        
        follow.delete()
        return Response({"status": "Unfollowed successfully"}, status=status.HTTP_200_OK)

    def list_following(self, request):
        following = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_followers(self, request):
        followers = Follow.objects.filter(following=request.user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowRequestViewSet(viewsets.ViewSet):
    def send_request(self, request, user_id=None):
        requester = request.user
        if requester.id == user_id:
            return Response({"error": "Cannot send follow request to self"}, status=status.HTTP_400_BAD_REQUEST)
        
        recipient = User.objects.filter(id=user_id).first()
        if not recipient:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        follow_request, created = FollowRequest.objects.get_or_create(requester=requester, recipient=recipient)
        if not created:
            return Response({"status": "Follow request already sent"}, status=status.HTTP_200_OK)

        serializer = FollowRequestSerializer(follow_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def accept_request(self, request, request_id=None):
        follow_request = FollowRequest.objects.filter(id=request_id, recipient=request.user, status='pending').first()
        if not follow_request:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)
        
        follow_request.status = 'accepted'
        follow_request.save()
        Follow.objects.create(follower=follow_request.requester, following=request.user)

        return Response({"status": "Follow request accepted"}, status=status.HTTP_200_OK)

    def cancel_request(self, request, request_id=None):
        follow_request = FollowRequest.objects.filter(id=request_id, requester=request.user, status='pending').first()
        if not follow_request:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        follow_request.status = 'cancelled'
        follow_request.save()
        return Response({"status": "Follow request cancelled"}, status=status.HTTP_200_OK)

class BlockViewSet(viewsets.ViewSet):
    def block_user(self, request, user_id=None):
        blocker = request.user
        blocked = User.objects.filter(id=user_id).first()
        if not blocked:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        reason = request.data.get("reason", "")
        block, created = Block.objects.get_or_create(blocker=blocker, blocked=blocked, defaults={"reason": reason})
        if not created:
            return Response({"status": "User already blocked"}, status=status.HTTP_200_OK)

        serializer = BlockSerializer(block)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unblock_user(self, request, user_id=None):
        block = Block.objects.filter(blocker=request.user, blocked_id=user_id).first()
        if not block:
            return Response({"error": "User not blocked"}, status=status.HTTP_404_NOT_FOUND)
        
        block.delete()
        return Response({"status": "User unblocked successfully"}, status=status.HTTP_200_OK)
