from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Profile, Role, Industry, Skill, Experience, Education
from .serializers import (
    ExperienceSerializer, EducationSerializer, ProfileCreateSerializer, RoleSerializer,IndustrySerializer,
    SkillSerializer,
)

User = get_user_model()
     
# View to list all available roles
class RoleListView(viewsets.ViewSet):
    def list(self, request):
        roles = Role.objects.all()
        if not roles.exists():
            return Response({
                "status": "error",
                "message": "No roles available",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(roles, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# View to list all industries
class IndustryListView(viewsets.ViewSet):
    def list(self, request):
        industries = Industry.objects.all()
        if not industries.exists():
            return Response({
                "status": "error",
                "message": "No industries found",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = IndustrySerializer(industries, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# View to list all skills
class SkillListView(viewsets.ViewSet):
    def list(self, request):
        skills = Skill.objects.all()
        if not skills.exists():
            return Response({
                "status": "error",
                "message": "No skills found",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SkillSerializer(skills, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

        
# Role selection view
class RoleSelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        # Validate input
        if not user_id:
            return Response({"error": "user_id is a required field."}, status=status.HTTP_400_BAD_REQUEST)
        if not role_id:
            return Response({"error": "role_id is a required field."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists in the CustomUser model
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "User not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if the role exists
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Role not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if a Profile already exists for this user, if not, create one
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Assign the selected role to the profile
        profile.selected_role = role
        profile.save()

        # Return success response
        return Response({
            "status": "success",
            "message": "Role selected successfully",
            "data": {
                "role": role.role_name,
                "id": role.id
            }
        }, status=status.HTTP_200_OK)

# Primary industry selection view
class PrimaryIndustrySelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        industry_id = request.data.get('industry_id')

        if not user_id or not industry_id:
            raise ValidationError({"error": "user_id and industry_id are required fields."})

        try:
            profile = Profile.objects.get(user_id=user_id)
            industry = Industry.objects.get(id=industry_id)
            profile.selected_primary_industry = industry
            profile.save()

            return Response({
                "status": "success",
                "message": "Primary industry selected successfully",
                "data": {
                    "industry": industry.name,
                    "id": industry.id
                }
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Profile not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)
        except Industry.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Industry not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

# Primary skill selection view
class PrimarySkillSelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        skill_id = request.data.get('skill_id')

        if not user_id or not skill_id:
            raise ValidationError({"error": "user_id and skill_id are required fields."})

        try:
            profile = Profile.objects.get(user_id=user_id)
            skill = Skill.objects.get(id=skill_id)
            profile.selected_primary_skill = skill
            profile.save()

            return Response({
                "status": "success",
                "message": "Primary skill selected successfully",
                "data": {
                    "skill": skill.name,
                    "id": skill.id
                }
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Profile not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)
        except Skill.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Skill not found",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

# Experience viewset for listing and adding experiences
class ExperienceViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        experiences = Experience.objects.filter(user_id=user_id)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Experience added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Education viewset for listing and adding education
class EducationViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        education = Education.objects.filter(user_id=user_id)
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Education added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile creation view
class ProfileCreateView(viewsets.ViewSet):
    def create(self, request):
        serializer = ProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Profile created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

