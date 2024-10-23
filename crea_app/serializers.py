from rest_framework import serializers
from .models import CustomUser, OTPVerification
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser
from .models import OnboardingImage


class OnboardingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingImage
        fields = ['id', 'title', 'short_description', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Ensure no double URL in the image field
        image_url = representation.get('image', '')
        if image_url.startswith('https://s3.us-east-005.backblazeb2.com'):
            # Avoid duplicate URLs by trimming redundant part
            representation['image'] = image_url.replace(
                'https://s3.us-east-005.backblazeb2.com/file/crea-onboarding/https://s3.us-east-005.backblazeb2.com/file/crea-onboarding/', 
                'https://s3.us-east-005.backblazeb2.com/file/crea-onboarding/'
            )

        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'mobile_or_email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'mobile_or_email', 'password', 'login_method','device_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['user','mobile_or_email', 'otp', 'otp_expires_at', 'is_verified']


    
class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    mobile_or_email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)
    
    def validate_user_id(self, value):
        User = get_user_model()
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

