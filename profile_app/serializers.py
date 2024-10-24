from rest_framework import serializers
from .models import UserProfile, Industry, Skill
from .models import AadharVerification
from .models import PassportVerification,DriverLicenseVerification
from rest_framework import serializers
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    mobile_or_email = serializers.CharField(source='user.mobile_or_email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user_id', 'mobile_or_email', 'user_type', 
            'selected_industries', 'selected_primary_industry', 
            'selected_skills', 'selected_primary_skill',
            'cover_image', 'profile_image', 'bio', 
            'date_of_birth', 'age', 'location', 'height', 'weight'
        ]

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'industry_image']

class SkillSerializer(serializers.ModelSerializer):
    industry_belong = serializers.CharField(source='industry.name', read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'skill_image', 'industry_belong']


class AadharVerificationSerializer(serializers.ModelSerializer):
    mobile_or_email = serializers.CharField(required=True)

    class Meta:
        model = AadharVerification
        fields = ['mobile_or_email', 'aadhar_cn', 'aadhar_fname', 'verify_status']
        read_only_fields = ['verify_status']

    def validate_aadhar_cn(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Aadhar number must be a 12-digit number.")
        return value

    def create(self, validated_data):
        mobile_or_email = validated_data.pop('mobile_or_email')
        User = get_user_model()
        
        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        aadhar_verification = AadharVerification.objects.create(user=user, **validated_data)
        return aadhar_verification


class PassportVerificationSerializer(serializers.ModelSerializer):
    mobile_or_email = serializers.CharField(required=True)

    class Meta:
        model = PassportVerification
        fields = ['mobile_or_email', 'ps_cn', 'ps_fname', 'ps_isscountry', 'ps_dateexp', 'verify_status']
        read_only_fields = ['verify_status']

    def validate_ps_cn(self, value):
        if len(value) < 8 or len(value) > 12:
            raise serializers.ValidationError("Passport number must be between 8 to 12 characters.")
        return value

    def create(self, validated_data):
        mobile_or_email = validated_data.pop('mobile_or_email')
        User = get_user_model()
        
        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        passport_verification = PassportVerification.objects.create(user=user, **validated_data)
        return passport_verification


class DriverLicenseVerificationSerializer(serializers.ModelSerializer):
    mobile_or_email = serializers.CharField(required=True)

    class Meta:
        model = DriverLicenseVerification
        fields = ['mobile_or_email', 'dl_ln', 'dl_fname', 'dl_isscstate', 'verify_status']
        read_only_fields = ['verify_status']

    def validate_dl_ln(self, value):
        if len(value) < 5 or len(value) > 15:  # Adjust based on your needs
            raise serializers.ValidationError("Driver's License number must be between 5 to 15 characters.")
        return value

    def create(self, validated_data):
        mobile_or_email = validated_data.pop('mobile_or_email')
        User = get_user_model()
        
        try:
            user = User.objects.get(mobile_or_email=mobile_or_email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        dl_verification = DriverLicenseVerification.objects.create(user=user, **validated_data)
        return dl_verification
