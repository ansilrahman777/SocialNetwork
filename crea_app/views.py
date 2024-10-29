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
from firebase_admin import auth as firebase_auth
from rest_framework_simplejwt.tokens import RefreshToken


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

    def post(self, request):
        # Get the login method and tokens
        login_method = request.data.get('login_method')  # "1" for traditional, "2" for Google, "3" for Apple
        mobile_or_email = request.data.get('mobile_or_email')
        password = request.data.get('password')
        google_token = request.data.get('google_token')
        apple_token = request.data.get('apple_token')

        # Validate input
        if login_method not in ["1", "2", "3"]:
            return Response({
                "status": "error",
                "message": "Invalid login method"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Handle traditional login (email/password)
            if login_method == "1":
                return self.handle_traditional_login(mobile_or_email, password)

            # Handle Google login
            elif login_method == "2":
                return self.handle_google_login(google_token)

            # Handle Apple login
            elif login_method == "3":
                return self.handle_apple_login(apple_token)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_traditional_login(self, mobile_or_email, password):
        try:
            user = CustomUser.objects.get(mobile_or_email=mobile_or_email)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return self.generate_response(user, refresh, "1")  # Pass "1" for traditional login
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

    def handle_google_login(self, google_token):
        if not google_token:
            return Response({
                "status": "error",
                "message": "Google token must not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = firebase_auth.verify_id_token(google_token)
            email = decoded_token.get('email')

            user, _ = CustomUser.objects.get_or_create(
                mobile_or_email=email,
                defaults={"user_status": "active"}
            )
            refresh = RefreshToken.for_user(user)
            return self.generate_response(user, refresh, "2")  # Pass "2" for Google login

        except firebase_auth.InvalidIdTokenError:
            return Response({
                "status": "error",
                "message": "Invalid Google token."
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_apple_login(self, apple_token):
        if not apple_token:
            return Response({
                "status": "error",
                "message": "Apple token must not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = firebase_auth.verify_id_token(apple_token)
            email = decoded_token.get('email')

            user, _ = CustomUser.objects.get_or_create(
                mobile_or_email=email,
                defaults={"user_status": "active"}
            )
            refresh = RefreshToken.for_user(user)
            return self.generate_response(user, refresh, "3")  # Pass "3" for Apple login

        except firebase_auth.InvalidIdTokenError:
            return Response({
                "status": "error",
                "message": "Invalid Apple token."
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Helper function to generate the response with tokens
    def generate_response(self, user, refresh, login_method):
        return Response({
            "status": {
                "type": "success",
                "message": "Logged in successfully",
                "code": 200,
                "error": False
            },
            "data": [{
                "status": "Authenticated",
                "user": {
                    "email": user.mobile_or_email,
                    "user_id": user.id,
                    "user_status": user.user_status,
                    "login_method": login_method,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }]
        }, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')
        otp_received = request.data.get('otp')
        action = request.data.get('action')  # This can be 'reset_password' or 'login'

        User = get_user_model()

        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
            otp_verification = OTPVerification.objects.get(user=user, otp=otp_received)

            if timezone.now() > otp_verification.otp_expires_at:
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the OTP as verified
            otp_verification.is_verified = True
            otp_verification.save()

            if action == 'reset_password':
                # Here you can return a success response for password reset
                return Response({
                    "status": {
                        "type": "success",
                        "message": "OTP verified successfully. You can now set a new password.",
                        "code": 200,
                        "error": False
                    },
                    "data": [{
                        "status": "Verified for password reset"
                    }]
                }, status=status.HTTP_200_OK)

            # Other actions (e.g., login) can be handled here
            return Response({
                "status": {
                    "type": "success",
                    "message": "OTP verified successfully. You are logged in.",
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
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')

        User = get_user_model()

        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
            # Fetch all OTPs for the user
            otp_verifications = OTPVerification.objects.filter(user=user)

            if otp_verifications.exists():
                # Choose the latest OTP that hasn't been verified or expired
                latest_otp = otp_verifications.order_by('-otp_expires_at').first()

                # If the latest OTP is not expired, resend it
                if latest_otp and latest_otp.is_verified is False and latest_otp.otp_expires_at > timezone.now():
                    otp = latest_otp.otp
                else:
                    # Generate a new OTP if the latest one is expired or verified
                    otp = str(random.randint(100000, 999999))
                    OTPVerification.objects.create(user=user, otp=otp)

                # Send the OTP via email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}. It is valid for 10 minutes.',
                    settings.EMAIL_HOST_USER,
                    [user.mobile_or_email],
                    fail_silently=False,
                )

                return Response({
                    "status": {
                        "type": "success",
                        "message": "OTP sent successfully to your Email address.",
                        "code": 200,
                        "error": False
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                "status": {
                    "type": "error",
                    "message": "No OTP entries found for this user.",
                    "code": 404,
                    "error": True
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({
                "status": {
                    "type": "error",
                    "message": "User not found.",
                    "code": 404,
                    "error": True
                }
            }, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')
        new_password = request.data.get('new_password')
        otp_received = request.data.get('otp')

        User = get_user_model()

        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
            otp_verification = OTPVerification.objects.get(user=user, otp=otp_received)

            if timezone.now() > otp_verification.otp_expires_at:
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the OTP as verified
            otp_verification.is_verified = True
            otp_verification.save()

            # Set new password
            user.set_password(new_password)
            user.save()

            return Response({
                "status": {
                    "type": "success",
                    "message": "Password reset successfully",
                    "code": 200,
                    "error": False
                }
            }, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


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
        