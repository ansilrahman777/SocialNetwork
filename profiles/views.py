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


class UserProfileView(APIView):
    @swagger_auto_schema(request_body=UserProfileSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Save or update user profile
            serializer.save()

            return Response({
                "status": {
                    "type": "success",
                    "message": "Profile updated successfully",
                    "code": 200,
                    "error": False
                },
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
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
    def post(self, request):
        user_id = request.data.get('user_id')
        mobile_or_email = request.data.get('mobile_or_email')

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
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SkillListView(APIView):
    def post(self, request):
        user_id = request.data.get('User_id')
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
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)