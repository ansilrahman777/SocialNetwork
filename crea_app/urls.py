# urls.py

from django.urls import path
from .views import RegisterView, LoginView, VerifyOTPView, ResendOTPView,LogoutView
from .views import ResetPasswordView, ChangePasswordView
from .views import OnboardingAPIView



urlpatterns = [

    path('onboardingcrea/', OnboardingAPIView.as_view(), name='onboarding-create'),
    path('onboardingcrea/<int:pk>/', OnboardingAPIView.as_view(), name='onboarding-update-delete'),
    path('registercrea/', RegisterView.as_view(), name='register'),
    path('logincrea/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verifyotp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resendotp/', ResendOTPView.as_view(), name='resend_otp'),
    path('profile/resetpassword/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/changepassword/', ChangePasswordView.as_view(), name='change-password'),
    
]