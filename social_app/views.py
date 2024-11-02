from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Follow, FollowRequest, Block
from .serializers import FollowRequestSerializer, FollowSerializer, BlockSerializer
from django.contrib.auth import get_user_model
from userprofile_app.models import Profile, Role

User = get_user_model()

class ListFollowersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        followers = Follow.objects.filter(following=user)
        data = []
        for follower in followers:
            follower_user = follower.follower
            try:
                follower_profile = Profile.objects.get(user=follower_user)
                role_name = follower_profile.selected_role.role_name if follower_profile.selected_role else ""
                profile_pic_url = follower_profile.profile_image or ""
            except Profile.DoesNotExist:
                role_name = ""
                profile_pic_url = ""
            data.append({
                "follower_id": str(follower_user.id),
                "name": follower_user.username or "",
                "role": role_name,
                "profile_pic_url": profile_pic_url
            })

        return Response({
            "user_id": str(user_id),
            "followers": data
        }, status=status.HTTP_200_OK)

class ListFollowingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        following = Follow.objects.filter(follower=user)
        data = []
        for follow in following:
            following_user = follow.following
            try:
                following_profile = Profile.objects.get(user=following_user)
                role_name = following_profile.selected_role.role_name if following_profile.selected_role else ""
                profile_pic_url = following_profile.profile_image or ""
            except Profile.DoesNotExist:
                role_name = ""
                profile_pic_url = ""
            data.append({
                "followed_id": str(following_user.id),
                "name": following_user.username or "",
                "role": role_name,
                "profile_pic_url": profile_pic_url
            })

        return Response({
            "user_id": str(user_id),
            "following": data
        }, status=status.HTTP_200_OK)

class FollowRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def send_request(self, request, user_id=None):
        requester = request.user
        if int(requester.id) == int(user_id):
            return Response({"error": "You cannot send a follow request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recipient = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if Block.objects.filter(blocker=recipient, blocked=requester).exists():
            return Response({"error": "You are blocked by this user."}, status=status.HTTP_403_FORBIDDEN)

        if FollowRequest.objects.filter(requester=requester, recipient=recipient, status='pending').exists():
            return Response({"error": "Follow request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(follower=requester, following=recipient).exists():
            return Response({"error": "User is already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = FollowRequest.objects.create(requester=requester, recipient=recipient)
        return Response({
            "message": "Follow request sent successfully",
            "data": {
                "user_id": str(recipient.id),
                "follower_id": str(requester.id),
                "requested_at": follow_request.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)

    def accept_request(self, request, user_id=None):
        recipient = request.user
        try:
            follow_request = FollowRequest.objects.get(requester_id=user_id, recipient=recipient, status='pending')
        except FollowRequest.DoesNotExist:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        follow_request.status = 'accepted'
        follow_request.save()
        follow = Follow.objects.create(follower=follow_request.requester, following=recipient)

        return Response({
            "message": "Follow request accepted",
            "data": {
                "user_id": str(follow.following.id),
                "follower_id": str(follow.follower.id),
                "followed_at": follow.followed_at.isoformat()
            }
        }, status=status.HTTP_200_OK)

    def cancel_request(self, request, user_id=None):
        requester = request.user
        try:
            follow_request = FollowRequest.objects.get(requester=requester, recipient_id=user_id, status='pending')
        except FollowRequest.DoesNotExist:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        follow_request.status = 'cancelled'
        follow_request.save()
        return Response({
            "success": True,
            "message": "Follow request canceled."
        }, status=status.HTTP_200_OK)

    def unfollow(self, request, user_id=None):
        follower = request.user
        try:
            follow = Follow.objects.get(follower=follower, following_id=user_id)
        except Follow.DoesNotExist:
            return Response({"error": "User is not currently following this user"}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response({
            "message": "Unfollowed successfully",
            "data": {
                "user_id": str(user_id),
                "follower_id": str(follower.id),
                "unfollowed_at": timezone.now().isoformat()
            }
        }, status=status.HTTP_200_OK)

    def list_requests(self, request):
        user = request.user
        follow_requests = FollowRequest.objects.filter(recipient=user, status='pending')
        data = []
        for req in follow_requests:
            requester = req.requester
            try:
                requester_profile = Profile.objects.get(user=requester)
                profile_pic_url = requester_profile.profile_image or ""
                role_name = requester_profile.selected_role.role_name if requester_profile.selected_role else ""
            except Profile.DoesNotExist:
                profile_pic_url = ""
                role_name = ""
            data.append({
                "requester_id": str(requester.id),
                "name": requester.username or "",
                "role": role_name,
                "profile_pic_url": profile_pic_url,
                "requested_at": req.created_at.isoformat()
            })
        return Response({
            "user_id": str(user.id),
            "follow_requests": data
        }, status=status.HTTP_200_OK)

class BlockViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def block_user(self, request, user_id=None):
        blocker = request.user
        if int(blocker.id) == int(user_id):
            return Response({"error": "You cannot block yourself."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            blocked_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if Block.objects.filter(blocker=blocker, blocked=blocked_user).exists():
            return Response({"error": "User is already blocked"}, status=status.HTTP_400_BAD_REQUEST)

        reason = request.data.get("reason", "")
        block = Block.objects.create(blocker=blocker, blocked=blocked_user, reason=reason)
        return Response({
            "success": True,
            "message": "User has been successfully blocked.",
            "data": {
                "blocked_user_id": str(blocked_user.id),
                "reason": reason,
                "blocked_at": block.blocked_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)

    def unblock_user(self, request, user_id=None):
        blocker = request.user
        try:
            block = Block.objects.get(blocker=blocker, blocked_id=user_id)
        except Block.DoesNotExist:
            return Response({"error": "User not blocked"}, status=status.HTTP_404_NOT_FOUND)

        block.delete()
        return Response({
            "success": True,
            "message": "User unblocked successfully"
        }, status=status.HTTP_200_OK)
