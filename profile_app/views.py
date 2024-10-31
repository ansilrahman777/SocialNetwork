from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import UserProfile, Industry, Skill
from .serializers import UserProfileSerializer, IndustrySerializer, SkillSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from .serializers import AadharVerificationSerializer
from .serializers import DriverLicenseVerificationSerializer,PassportVerificationSerializer
from crea_app.backblaze_storage import BackblazeStorage
from .models import CustomUser



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


class AadharVerificationView(APIView):
    def post(self, request):
        data = request.data.copy()
        mobile_or_email = data.get("mobile_or_email")

        if not mobile_or_email:
            return Response({
                "status": {
                    "type": "error",
                    "message": "mobile_or_email is required.",
                    "code": 400,
                    "error": True
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user based on mobile_or_email
        try:
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)
            data['user'] = user.id  # Assuming your serializer requires a user field
        except CustomUser.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "message": "User not found.",
                    "code": 404,
                    "error": True
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AadharVerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": {
                    "type": "success",
                    "message": "Aadhar Update Successfully",
                    "code": 200,
                    "error": False
                },
                "data": [
                    {
                        "status": "Document pending",
                        "verify_status": "1"
                    }
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PassportVerificationView(APIView):
    def post(self, request):
        data = request.data.copy()
        mobile_or_email = data.get("mobile_or_email")

        if not mobile_or_email:
            return Response({
                "status": {
                    "type": "error",
                    "message": "mobile_or_email is required.",
                    "code": 400,
                    "error": True
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)
            data['user'] = user.id
        except CustomUser.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "message": "User not found.",
                    "code": 404,
                    "error": True
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PassportVerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": {
                    "type": "success",
                    "message": "Passport Update Successfully",
                    "code": 200,
                    "error": False
                },
                "data": [
                    {
                        "status": "Document pending",
                        "verify_status": "2"
                    }
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DriverLicenseVerificationView(APIView):
    def post(self, request):
        data = request.data.copy()
        mobile_or_email = data.get("mobile_or_email")

        if not mobile_or_email:
            return Response({
                "status": {
                    "type": "error",
                    "message": "mobile_or_email is required.",
                    "code": 400,
                    "error": True
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)
            data['user'] = user.id
        except CustomUser.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "message": "User not found.",
                    "code": 404,
                    "error": True
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverLicenseVerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": {
                    "type": "success",
                    "message": "Driver’s License Update Successfully",
                    "code": 200,
                    "error": False
                },
                "data": [
                    {
                        "status": "Verification Completed",
                        "verify_status": "3"
                    }
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
