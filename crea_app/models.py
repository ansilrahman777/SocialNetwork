from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_or_email, password=None, **extra_fields):
        if not mobile_or_email:
            raise ValueError('The mobile or email field must be set')
        user = self.model(mobile_or_email=mobile_or_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_or_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile_or_email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    mobile_or_email = models.CharField(unique=True, max_length=255)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    device_model = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    device_ipaddress = models.CharField(max_length=45, null=True, blank=True)
    login_method = models.CharField(max_length=50, choices=[('1', 'Traditional'), ('google', 'Google'), ('apple', 'Apple')])
    user_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_or_email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile_or_email

class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_verifications')
    otp = models.CharField(max_length=6)
    otp_expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.otp_expires_at:
            self.otp_expires_at = timezone.now() + timezone.timedelta(minutes=10)  # OTP expiry time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP for {self.user.mobile_or_email}"

class UserSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)  # Default session expiry
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session for {self.user.mobile_or_email}"


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    reset_token = models.CharField(max_length=255)
    otp_expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.otp_expires_at


class OnboardingImage(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    image = models.ImageField(upload_to='onboarding-images/', default='onboarding-images/default.jpg')

    def __str__(self):
        return self.title
