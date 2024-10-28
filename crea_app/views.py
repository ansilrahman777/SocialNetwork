from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .serializers import LogoutSerializer, UserSerializer, RegisterSerializer, OTPSerializer, ResetPasswordSerializer, ChangePasswordSerializer, OnboardingImageSerializer
from .models import CustomUser, OTPVerification, UserSession, OnboardingImage, PasswordResetRequest
from .backblaze_storage import upload_to_backblaze
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


CustomUser = get_user_model()



class OnboardingAPIView(APIView):
    permission_classes = [AllowAny]  
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
            # Retrieve user by mobile/email
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)

            # Check password
            if user.check_password(password):
                # Generate access and refresh tokens
                refresh = RefreshToken.for_user(user)

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
                        "tokens": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    }]
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error", 
                    "message": "Invalid password"
                }, status=status.HTTP_401_UNAUTHORIZED)

        except CustomUser.DoesNotExist:
            return Response({
                "status": "error", 
                "message": "User does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

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


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Ensure this is defined correctly
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mobile_or_email = serializer.validated_data['mobile_or_email']
            
            try:
                # Find user by mobile or email
                user = CustomUser.objects.get(mobile_or_email=mobile_or_email)
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
    authentication_classes = [JWTAuthentication]  # Enforce JWT-based authentication
    permission_classes = [IsAuthenticated]        # Ensure only authenticated users can access
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            user = request.user  # Get the authenticated user

            # Check if the current password is correct
            if not check_password(current_password, user.password):
                return Response({
                    "status": {
                        "type": "error",
                        "message": "Current password is incorrect",
                        "code": 400,
                        "error": True
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # Ensure new password matches confirm password
            if new_password != confirm_password:
                return Response({
                    "status": {
                        "type": "error",
                        "message": "New password and confirm password do not match",
                        "code": 400,
                        "error": True
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password and save the user
            user.set_password(new_password)
            user.save()

            return Response({
                "status": {
                    "type": "success",
                    "message": "Password changed successfully",
                    "code": 200,
                    "error": False
                },
                "data": {
                    "user": {
                        "user_id": user.id,
                        "status": "Password changed"
                    }
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Invalid input",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']

        try:
            # Blacklist the refresh token
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({
                "status": {
                    "type": "success",
                    "message": "Successfully logged out",
                    "code": 200,
                    "error": False
                }
            }, status=status.HTTP_205_RESET_CONTENT)

        except OutstandingToken.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "message": "Token not found or already blacklisted",
                    "code": 400,
                    "error": True
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": {
                    "type": "error",
                    "message": str(e),
                    "code": 400,
                    "error": True
                }
            }, status=status.HTTP_400_BAD_REQUEST)