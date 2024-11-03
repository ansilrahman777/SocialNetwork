from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Follow, FollowRequest, Block, Report
from .serializers import FollowRequestSerializer, FollowSerializer, BlockSerializer, ReasonSerializer, ReportSerializer
from django.contrib.auth import get_user_model
from userprofile_app.models import Profile, Role

User = get_user_model()

def is_blocked(user, target_user):
    """ Check if 'target_user' is blocked by 'user'. """
    return Block.objects.filter(blocker=user, blocked=target_user).exists() or Block.objects.filter(blocker=target_user, blocked=user).exists()

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
        try:
            recipient = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if is_blocked(requester, recipient):
            return Response({"error": "You cannot follow this user."}, status=status.HTTP_403_FORBIDDEN)

        # Prevent self-follow requests
        if int(requester.id) == int(user_id):
            return Response({"error": "You cannot send a follow request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the recipient exists
        try:
            recipient = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if requester is blocked by the recipient
        if Block.objects.filter(blocker=recipient, blocked=requester).exists():
            return Response({"error": "You are blocked by this user."}, status=status.HTTP_403_FORBIDDEN)

        # Check if there's an existing follow request or follow relationship
        follow_request = FollowRequest.objects.filter(requester=requester, recipient=recipient).first()
        follow_exists = Follow.objects.filter(follower=requester, following=recipient).exists()

        if follow_exists:
            return Response({"error": "User is already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        if follow_request:
            # If the request is pending, don't allow another request to be sent
            if follow_request.status == 'pending':
                return Response({"error": "Follow request is already pending"}, status=status.HTTP_400_BAD_REQUEST)

            # If the request was previously accepted or canceled, update it to pending
            follow_request.status = 'pending'
            follow_request.save()
            return Response({
                "message": "Follow request re-sent successfully",
                "data": {
                    "user_id": str(recipient.id),
                    "follower_id": str(requester.id),
                    "requested_at": follow_request.created_at.isoformat()
                }
            }, status=status.HTTP_200_OK)

        # Create a new follow request if none exists
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
        """Allows the requester to cancel a pending follow request."""
        requester = request.user

        # Ensure only the requester can cancel their own follow request
        try:
            follow_request = FollowRequest.objects.get(
                requester=requester, recipient_id=user_id, status='pending'
            )
        except FollowRequest.DoesNotExist:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        # Cancel the follow request if it's pending
        follow_request.status = 'cancelled'
        follow_request.save()
        return Response({
            "success": True,
            "message": "Follow request canceled."
        }, status=status.HTTP_200_OK)

    def reject_request(self, request, user_id=None):
        """Allows the recipient to reject a pending follow request."""
        recipient = request.user

        # Ensure only the recipient can reject a follow request they received
        try:
            follow_request = FollowRequest.objects.get(
                requester_id=user_id, recipient=recipient, status='pending'
            )
        except FollowRequest.DoesNotExist:
            return Response({"error": "Follow request not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        # Reject the follow request if it's pending
        follow_request.status = 'rejected'
        follow_request.save()
        return Response({
            "success": True,
            "message": "Follow request rejected."
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

        # Remove existing follow relationship
        Follow.objects.filter(follower=blocked_user, following=blocker).delete()
        Follow.objects.filter(follower=blocker, following=blocked_user).delete()

        # Create the block record
        common_reason = request.data.get("common_reason")
        reason_details = request.data.get("reason_details", "")
        block = Block.objects.create(
            blocker=blocker, 
            blocked=blocked_user, 
            common_reason=common_reason, 
            reason_details=reason_details
        )

        return Response({
            "success": True,
            "message": "User has been successfully blocked.",
            "data": {
                "blocked_user_id": str(blocked_user.id),
                "common_reason": common_reason,
                "reason_details": reason_details,
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

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def report_user(self, request, user_id=None):
        reporter = request.user
        if int(reporter.id) == int(user_id):
            return Response({"error": "You cannot report yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            reported_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['reported'] = user_id
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            report = serializer.save(reporter=reporter)
            return Response({
                "success": True,
                "message": "User has been successfully reported.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockReasonListView(APIView):
    def get(self, request):
        reasons = [{'code': code, 'label': label} for code, label in Block.COMMON_BLOCK_REASONS]
        serializer = ReasonSerializer(reasons, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

class ReportReasonListView(APIView):
    def get(self, request):
        reasons = [{'code': code, 'label': label} for code, label in Report.COMMON_REPORT_REASONS]
        serializer = ReasonSerializer(reasons, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)