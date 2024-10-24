from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import UserProfile, Industry, Skill
from .serializers import UserProfileSerializer, IndustrySerializer, SkillSerializer
from drf_yasg.utils import swagger_auto_schema

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response({'status': 'success', 'data': serializer.data})
    except UserProfile.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user instance
        data = request.data.copy()
        data['user'] = user.id  # This is correct, user.id is an integer

        try:
            # Try to get the existing user profile
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile, data=data, partial=True)
            message = "Profile updated successfully"
            status_code = status.HTTP_200_OK
        except UserProfile.DoesNotExist:
            # If the user profile does not exist, create a new one
            serializer = UserProfileSerializer(data=data)
            message = "Profile created successfully"
            status_code = status.HTTP_201_CREATED

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()  # Save the serializer which now has the correct user instance
            return Response({
                "status": {
                    "type": "success",
                    "message": message,
                    "code": status_code,
                    "error": False
                },
                "data": serializer.data
            }, status=status_code)

        return Response({
            "status": {
                "type": "error",
                "message": "Invalid data",
                "code": status.HTTP_400_BAD_REQUEST,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class IndustryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        industries = Industry.objects.all()
        serializer = IndustrySerializer(industries, many=True)
        return Response({
            "status": {"type": "success", "message": "Overall Industry Data Found", "code": 200, "error": False},
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class SkillListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        industry_ids = request.data.get('industry_id', '').split(',')
        skills = Skill.objects.filter(industry__id__in=industry_ids)
        serializer = SkillSerializer(skills, many=True)

        return Response({
            "status": {"type": "success", "message": "Overall Skills Data Found", "code": 200, "error": False},
            "data": serializer.data,
            "user_id": user.id,
            "mobile_or_email": user.mobile_or_email
        }, status=status.HTTP_200_OK)
