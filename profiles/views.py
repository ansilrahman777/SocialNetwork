from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Industry, Skill
from .serializers import IndustrySerializer, SkillSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except UserProfile.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'User not found'
        }, status=404)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        data = request.data.copy()
        data['user_id'] = user.id  # Set the user_id from authenticated user

        # Check if the profile already exists for the user
        try:
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile, data=data, partial=True)  # Allow partial update
            message = "Profile updated successfully"
        except UserProfile.DoesNotExist:
            serializer = UserProfileSerializer(data=data)
            message = "Profile created successfully"

        # Validate and save the profile data
        if serializer.is_valid():
            serializer.save()  # Save the profile data

            return Response({
                "status": {
                    "type": "success",
                    "message": message,
                    "code": 200,
                    "error": False
                },
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)  # Return 201 for created

        return Response({
            "status": {
                "type": "error",
                "message": "Invalid data",
                "code": 400,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class IndustryListView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        user = request.user  # This will now be an authenticated user

        # Get the user_id and mobile_or_email from the custom user model
        user_id = user.id  # Get the authenticated user's ID
        mobile_or_email = user.mobile_or_email  # Get the mobile or email from the user

        # You can add user validation logic here if needed

        industries = Industry.objects.all()
        serializer = IndustrySerializer(industries, many=True)
        response_data = {
            "status": {
                "type": "success",
                "message": "Overall Industry Data Found",
                "code": 200,
                "error": False
            },
            "data": serializer.data,
            "user_id": user_id,
            "mobile_or_email": mobile_or_email
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SkillListView(APIView):
    def post(self, request):
        user = request.user  # Get the currently logged-in user

        # Get the user_id and mobile_or_email from the custom user model
        user_id = user.id  # Or user.user_id if your custom model has a field named user_id
        mobile_or_email = user.mobile_or_email  # Assuming this field exists in your custom user model

        industry_ids = request.data.get('industry_id', '').split(',')

        # You can add user validation logic here if needed

        skills = Skill.objects.filter(industry__id__in=industry_ids)
        serializer = SkillSerializer(skills, many=True)
        response_data = {
            "status": {
                "type": "success",
                "message": "Overall Skills Data Found",
                "code": 200,
                "error": False
            },
            "data": serializer.data,
            "user_id": user_id,
            "mobile_or_email": mobile_or_email
        }
        return Response(response_data, status=status.HTTP_200_OK)
