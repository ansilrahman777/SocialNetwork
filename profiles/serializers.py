from rest_framework import serializers
from .models import Industry, Skill
from .models import UserProfile
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    mobile_or_email = serializers.CharField(source='user.mobile_or_email', read_only=True)  # Assuming this field exists

    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'mobile_or_email', 'user_type', 'selected_industries',
            'selected_primary_industry', 'selected_skills', 'selected_primary_skill',
            'cover_image', 'profile_image', 'bio', 'date_of_birth', 'age', 
            'location', 'height', 'weight'
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