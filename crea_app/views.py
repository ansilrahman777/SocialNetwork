# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import CustomUser, OTPVerification, UserSession
from .serializers import UserSerializer,RegisterSerializer, OTPSerializer
from django.core.mail import send_mail
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
import random
from rest_framework import generics
from .models import PasswordResetRequest
from .serializers import ResetPasswordSerializer, ChangePasswordSerializer
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from .models import OnboardingImage
from .serializers import OnboardingImageSerializer
from .backblaze_storage import upload_to_backblaze 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


class OnboardingAPIView(APIView):
    def get(self, request, pk=None):
        # Check if a specific onboarding image is requested
        if pk:
            try:
                onboarding_image = OnboardingImage.objects.get(pk=pk)
            except OnboardingImage.DoesNotExist:
                return Response({
                    "status": {
                        "type": "error",
                        "code": 404,
                        "error": True
                    },
                    "message": "Onboarding image not found."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = OnboardingImageSerializer(onboarding_image)
        else:
            # Fetch all onboarding images
            onboarding_images = OnboardingImage.objects.all()
            serializer = OnboardingImageSerializer(onboarding_images, many=True)

        return Response({
            "status": {
                "type": "success",
                "code": 200,
                "error": False
            },
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({
                "status": {
                    "type": "error",
                    "code": 400,
                    "error": True
                },
                "message": "No image file provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = OnboardingImageSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = request.FILES['image']  # Get the uploaded image file
            user_id = request.data.get('user_id')  # Extract user_id from request data

            # Upload the file to Backblaze and get the image URL
            image_url = upload_to_backblaze(uploaded_file, user_id)

            # Save the serializer with the image URL
            onboarding_image = serializer.save(image=image_url)

            return Response({
                "status": {
                    "type": "success",
                    "code": 201,
                    "error": False
                },
                "data": {
                    "id": onboarding_image.id,  # Return the ID of the saved object
                    "title": onboarding_image.title,
                    "short_description": onboarding_image.short_description,
                    "image": image_url  # Include the uploaded image URL
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": {
                "type": "error",
                "code": 400,
                "error": True
            },
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            onboarding_image = OnboardingImage.objects.get(pk=pk)
        except OnboardingImage.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "code": 404,
                    "error": True
                },
                "message": "Onboarding image not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OnboardingImageSerializer(onboarding_image, data=request.data, partial=True)
        if serializer.is_valid():
            if 'image' in request.FILES:  # Check if there's a new image file to upload
                uploaded_file = request.FILES['image']
                user_id = request.data.get('user_id')  # Extract user_id from request data

                # Upload the file to Backblaze and get the new image URL
                image_url = upload_to_backblaze(uploaded_file, user_id)
                serializer.validated_data['image'] = image_url  # Update the image URL in serializer

            serializer.save()  # Save the updated onboarding image
            return Response({
                "status": {
                    "type": "success",
                    "code": 200,
                    "error": False
                },
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "code": 400,
                "error": True
            },
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            onboarding_image = OnboardingImage.objects.get(pk=pk)
            onboarding_image.delete()
            return Response({
                "status": {
                    "type": "success",
                    "code": 204,
                    "error": False
                },
                "message": "Onboarding image deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except OnboardingImage.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "code": 404,
                    "error": True
                },
                "message": "Onboarding image not found."
            }, status=status.HTTP_404_NOT_FOUND)



class RegisterView(APIView):
    permission_classes = [AllowAny]  # Ensure this is defined correctly
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = str(random.randint(100000, 999999))  # Generate a random OTP
            otp_verification = OTPVerification.objects.create(user=user, otp=otp)

            try:
                # Send OTP via Email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}. It is valid for 10 minutes.',
                    settings.EMAIL_HOST_USER,  # Use settings for email
                    [user.mobile_or_email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({
                    "status": {
                        "type": "error",
                        "message": "Failed to send OTP. Please try again.",
                        "code": 500,
                        "error": True
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "status": {
                    "type": "success",
                    "message": "OTP Sent to your Email address",
                    "code": 200,
                    "error": False
                },
                "data": [{
                    "status": "verification pending",
                    "user": {
                        "email": user.mobile_or_email,
                        "user_id": user.id,
                        "otp": otp,
                    },
                    "otpexpires_at": otp_verification.otp_expires_at
                }]
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)
            if user.check_password(password):
                # Generate or retrieve the token
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    "status": {
                        "type": "success",
                        "message": "Logged in Successfully",
                        "code": 200,
                        "error": False
                    },
                    "data": [{
                        "status": "Authenticated",
                        "user": {
                            "email": user.mobile_or_email,
                            "user_id": user.id,
                            "user_status": user.user_status,
                            "login_method": "1",
                        },
                        "token": token.key,  # Token returned here
                    }]
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')
        otp_received = request.data.get('otp_received')

        User = get_user_model()
        
        # Retrieve the user based on mobile or email
        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Now use the user to find the OTPVerification
        try:
            otp_verification = OTPVerification.objects.get(user=user, otp=otp_received)
            if timezone.now() > otp_verification.otp_expires_at:
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the OTP as verified
            otp_verification.is_verified = True
            otp_verification.save()

            # Optionally, generate a token or login user here
            # For example, you might want to create a token for the session

            return Response({
                "status": {
                    "type": "success",
                    "message": "Verified Successfully",
                    "code": 200,
                    "error": False
                },
                "data": [{
                    "status": "Authenticated"
                    # Include token or user information here if needed
                }]
            }, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')

        try:
            user = get_user_model().objects.get(mobile_or_email=mobile_or_email)
            otp = str(random.randint(100000, 999999))  # Generate a new OTP
            otp_verification = OTPVerification.objects.create(user=user, otp=otp)

            # Send new OTP via Email
            send_mail(
                'Your OTP Code',
                f'Your new OTP code is {otp}. It is valid for 10 minutes.',
                'your-email@gmail.com',  # From email
                [user.mobile_or_email],
                fail_silently=False,
            )

            return Response({
                "status": {
                    "type": "success",
                    "message": "OTP Sent to your Email address",
                    "code": 200,
                    "error": False
                },
                "data": [{
                    "status": "verification pending",
                    "otp": otp,
                    "otpexpires_at": otp_verification.otp_expires_at
                }]
            }, status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

CustomUser = get_user_model()

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            mobile_or_email = serializer.validated_data['mobile_or_email']
            
            try:
                # Update this line to use the correct field name
                user = CustomUser.objects.get(id=user_id, mobile_or_email=mobile_or_email)
                otp = str(random.randint(100000, 999999))  # Generate OTP
                reset_token = 'resetToken12345'  # In practice, generate a secure token
                
                PasswordResetRequest.objects.update_or_create(
                    user=user,
                    defaults={
                        'otp': otp,
                        'reset_token': reset_token,
                        'otp_expires_at': timezone.now() + timezone.timedelta(minutes=10),
                    }
                )

                send_mail(
                    'Your Password Reset OTP',
                    f'Your OTP is {otp}. It is valid for 10 minutes.',
                    'your-email@example.com',
                    [user.mobile_or_email],  # Send OTP to mobile_or_email
                    fail_silently=False,
                )

                return Response({
                    "status": {
                        "type": "success",
                        "message": "OTP Sent to your Email address or Mobile number.",
                        "code": 200,
                        "error": False
                    },
                    "data": [{
                        "status": "verification pending",
                        "user": {
                            "user_id": user.id,
                            "otp": otp,
                        },
                        "otpexpires_at": PasswordResetRequest.objects.get(user=user).otp_expires_at,
                    }]
                }, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({
                    "status": {
                        "type": "error",
                        "message": "User not found",
                        "code": 404,
                        "error": True
                    }
                }, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_password = serializer.validated_data['new_password']

            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(new_password)  # Set the new password
                user.save()

                return Response({
                    "status": {
                        "type": "success",
                        "message": "Password Reset Successfully",
                        "code": 200,
                        "error": False
                    },
                    "data": [{
                        "status": "Password Changed",
                        "user": {
                            "user_id": user.id,
                        },
                    }]
                }, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({
                    "status": {
                        "type": "error",
                        "message": "User not found",
                        "code": 404,
                        "error": True
                    }
                }, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


