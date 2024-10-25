# serializers.py
from rest_framework import serializers
from .models import Profile, Role, Industry, Skill, Experience, Education

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name', 'description']
        read_only_fields = ['id']  

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'image_url']
        read_only_fields = ['id']

class SkillSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)  

    class Meta:
        model = Skill
        fields = ['id', 'name', 'image_url', 'industry']
        read_only_fields = ['id']

class ExperienceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  

    class Meta:
        model = Experience
        fields = ['id', 'user', 'job_title', 'company_name', 'work_type', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['id']  

class EducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  

    class Meta:
        model = Education
        fields = ['id', 'user', 'degree', 'field_of_study', 'institution_name', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['id']  

class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  
    selected_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)  
    selected_primary_industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), write_only=True, allow_null=True)  
    selected_primary_skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), write_only=True, allow_null=True)  

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'mobile_or_email', 'user_type', 'selected_role', 'selected_primary_industry', 
            'selected_primary_skill', 'cover_image', 'profile_image', 'bio', 'date_of_birth', 
            'age', 'location', 'height', 'weight'
        ]
        read_only_fields = ['id', 'user'] 

class ProfileRoleSerializer(serializers.ModelSerializer):
    selected_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True) 

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_role']
        read_only_fields = ['user', 'mobile_or_email']  

class ProfilePrimaryIndustrySerializer(serializers.ModelSerializer):
    selected_primary_industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), write_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_primary_industry']
        read_only_fields = ['user', 'mobile_or_email']

class ProfilePrimarySkillSerializer(serializers.ModelSerializer):
    selected_primary_skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), write_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_primary_skill']
        read_only_fields = ['user', 'mobile_or_email']
