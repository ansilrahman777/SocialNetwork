import datetime
from rest_framework import serializers
from .models import DocumentUpload, Profile, Role, Industry, Skill, Experience, Education, AadharVerification, PassportVerification, DLVerification, UnionAssociation
from django.contrib.auth import get_user_model

User = get_user_model()
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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Allow writing user
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Experience
        fields = ['id', 'user', 'job_title', 'company_name', 'work_type', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['id']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after the start date.")
        
        return data

class EducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Allow writing user
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Education
        fields = ['id', 'user', 'degree', 'field_of_study', 'institution_name', 'start_date', 'end_date', 'is_current']
        read_only_fields = ['id']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after the start date.")
        
        return data

class ProfileCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    mobile_or_email = serializers.CharField(source='user.mobile_or_email', read_only=True)
    user_type = serializers.ChoiceField(choices=[('1', 'Admin'), ('2', 'Regular User')], default="2")
    selected_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)
    selected_primary_industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), required=False, allow_null=True)
    selected_primary_skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), required=False, allow_null=True)
    cover_image = serializers.FileField(required=False, allow_null=True)
    profile_image = serializers.FileField(required=False, allow_null=True)
    completion_percentage = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'mobile_or_email', 'user_type', 'selected_role', 'selected_primary_industry',
            'selected_primary_skill', 'cover_image', 'profile_image', 'bio', 'date_of_birth', 'age',
            'location', 'height', 'weight', 'view_count','followers_count', 'following_count', 'is_verified', 'completion_percentage'
        ]
        read_only_fields = ['id', 'user', 'view_count', 'is_verified', 'completion_percentage']
        
    def get_followers_count(self, obj):
        return obj.followers_count

    def get_following_count(self, obj):
        return obj.following_count

    def get_completion_percentage(self, obj):
        return obj.calculate_section_completion()
    
    def validate_cover_image(self, value):
        if value and not hasattr(value, 'size'):
            raise serializers.ValidationError("The cover_image provided is not a valid file.")
        return value

    def validate_profile_image(self, value):
        if value and not hasattr(value, 'size'):
            raise serializers.ValidationError("The profile_image provided is not a valid file.")
        return value

    def update(self, instance, validated_data):
        # Only delete the file if the field is set to None in the request and it currently has a file
        if 'profile_image' in validated_data and validated_data['profile_image'] is None and instance.profile_image:
            instance.profile_image.delete(save=False)  # Remove the file if set to null
        if 'cover_image' in validated_data and validated_data['cover_image'] is None and instance.cover_image:
            instance.cover_image.delete(save=False)
        
        return super().update(instance, validated_data)
    
class ProfileCompletionStatusSerializer(serializers.Serializer):
    totalCompletion = serializers.DictField()
    sections = serializers.ListField()
    pendingUpdates = serializers.ListField()
    verificationStatus = serializers.DictField()

# Profile Role Serializer
class ProfileRoleSerializer(serializers.ModelSerializer):
    selected_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_role']
        read_only_fields = ['user', 'mobile_or_email']

# Profile Primary Industry Serializer
class ProfilePrimaryIndustrySerializer(serializers.ModelSerializer):
    selected_primary_industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), required=True)

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_primary_industry']
        read_only_fields = ['user', 'mobile_or_email']

# Profile Primary Skill Serializer
class ProfilePrimarySkillSerializer(serializers.ModelSerializer):
    selected_primary_skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), required=True)

    class Meta:
        model = Profile
        fields = ['user', 'mobile_or_email', 'selected_primary_skill']
        read_only_fields = ['user', 'mobile_or_email']
        

class AadharVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharVerification
        fields = ['user', 'mobile_or_email', 'aadhar_cn', 'aadhar_fname', 'status', 'verify_status']
        read_only_fields = ['status', 'verify_status']

    def validate_aadhar_cn(self, value):
        if len(value) != 12 or not value.isdigit():
            raise serializers.ValidationError("Aadhar number must be exactly 12 digits.")
        return value

class PassportVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportVerification
        fields = ['user', 'mobile_or_email', 'ps_cn', 'ps_fname', 'ps_isscountry', 'ps_dateexp', 'status', 'verify_status']
        read_only_fields = ['status', 'verify_status']

    def validate_ps_cn(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Passport number must be at least 8 characters.")
        return value

    def validate_ps_dateexp(self, value):
        if value <= datetime.date.today():
            raise serializers.ValidationError("Passport expiry date must be in the future.")
        return value

class DLVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DLVerification
        fields = ['user', 'mobile_or_email', 'dl_ln', 'dl_fname', 'dl_isscstate', 'status', 'verify_status']
        read_only_fields = ['status', 'verify_status']

    def validate_dl_ln(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Driver's License number must be at least 6 characters.")
        return value


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['user', 'file', 'upload_status', 'verify_status']
        read_only_fields = ['upload_status', 'verify_status']

    def validate_file(self, value):
        allowed_formats = ['jpg', 'jpeg', 'png', 'pdf']
        extension = value.name.split('.')[-1].lower()
        if extension not in allowed_formats:
            raise serializers.ValidationError("File must be in JPG, PNG, or PDF format.")
        return value

class UnionAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnionAssociation
        fields = ['id', 'user', 'name', 'member_since']
        read_only_fields = ['id']

