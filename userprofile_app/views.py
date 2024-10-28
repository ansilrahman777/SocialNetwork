from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Profile, Role, Industry, Skill, Experience, Education
from .serializers import AadharVerificationSerializer, DLVerificationSerializer, DocumentUploadSerializer, ExperienceSerializer, EducationSerializer, PassportVerificationSerializer, ProfileCreateSerializer, RoleSerializer, IndustrySerializer, SkillSerializer

User = get_user_model()

def get_profile(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


class RoleListView(viewsets.ViewSet):
    def list(self, request):
        roles = Role.objects.all()
        if not roles.exists():
            return Response({"status": "error", "message": "No roles available"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(roles, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class RoleSelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        if not user_id or not role_id:
            return Response({"error": "user_id and role_id are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        role = Role.objects.filter(id=role_id).first()
        if not role:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.selected_role = role
        profile.save()

        return Response({"status": "success", "message": "Role selected successfully", "data": {"role": role.role_name, "id": role.id}}, status=status.HTTP_200_OK)

    def update(self, request, user_id=None):
        new_role_id = request.data.get('role_id')

        if not user_id or not new_role_id:
            return Response({"error": "user_id and role_id are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        new_role = Role.objects.filter(id=new_role_id).first()
        if not new_role:
            return Response({"error": "New role not found"}, status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.filter(user=user).first()
        if not profile:
            return Response({"error": "Profile not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_role = new_role
        profile.save()

        return Response({"status": "success", "message": "Role updated successfully", "data": {"role": new_role.role_name, "id": new_role.id}}, status=status.HTTP_200_OK)

class IndustryListView(viewsets.ViewSet):
    def list(self, request):
        industries = Industry.objects.all()
        if not industries.exists():
            return Response({"status": "error", "message": "No industries found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = IndustrySerializer(industries, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class IndustrySelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        industry_ids = request.data.get('industry_ids', [])

        if not user_id or not industry_ids:
            return Response({"error": "user_id and industry_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        industries = Industry.objects.filter(id__in=industry_ids)
        if industries.count() != len(industry_ids):
            return Response({"error": "Some industries are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_industries.set(industries)
        profile.save()

        return Response({"status": "success", "message": "Industries selected successfully", "data": {"selected_industries": industry_ids}}, status=status.HTTP_200_OK)

    def update(self, request, user_id=None):
        industry_ids = request.data.get('industry_ids', [])

        if not user_id or not industry_ids:
            return Response({"error": "user_id and industry_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        industries = Industry.objects.filter(id__in=industry_ids)
        if industries.count() != len(industry_ids):
            return Response({"error": "Some industries are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_industries.set(industries)
        profile.save()

        return Response({"status": "success", "message": "Industries updated successfully", "data": {"selected_industries": industry_ids}}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_industries.clear()
        profile.save()

        return Response({"status": "success", "message": "Industries removed successfully"}, status=status.HTTP_200_OK)


class PrimaryIndustrySelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        primary_industry_id = request.data.get('primary_industry_id')

        if not user_id or not primary_industry_id:
            return Response({"error": "user_id and primary_industry_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        primary_industry = Industry.objects.filter(id=primary_industry_id).first()
        if not primary_industry or primary_industry not in profile.selected_industries.all():
            return Response({"error": "Primary industry must be chosen from selected industries."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_primary_industry = primary_industry
        profile.save()

        return Response({"status": "success", "message": "Primary industry selected successfully", "data": {"primary_industry": primary_industry.name}}, status=status.HTTP_200_OK)

    def update(self, request, user_id=None):
        primary_industry_id = request.data.get('primary_industry_id')

        if not user_id or not primary_industry_id:
            return Response({"error": "user_id and primary_industry_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        primary_industry = Industry.objects.filter(id=primary_industry_id).first()
        if not primary_industry or primary_industry not in profile.selected_industries.all():
            return Response({"error": "Primary industry must be chosen from selected industries."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_primary_industry = primary_industry
        profile.save()

        return Response({"status": "success", "message": "Primary industry updated successfully", "data": {"primary_industry": primary_industry.name}}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_primary_industry = None
        profile.save()

        return Response({"status": "success", "message": "Primary industry removed successfully"}, status=status.HTTP_200_OK)

class SkillListView(viewsets.ViewSet):
    def list(self, request):
        skills = Skill.objects.all()
        if not skills.exists():
            return Response({"status": "error", "message": "No skills found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SkillSerializer(skills, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class SkillSelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        skill_ids = request.data.get('skill_ids', [])

        if not user_id or not skill_ids:
            return Response({"error": "user_id and skill_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        skills = Skill.objects.filter(id__in=skill_ids)
        if skills.count() != len(skill_ids):
            return Response({"error": "Some skills are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_skills.set(skills)
        profile.save()

        return Response({"status": "success", "message": "Skills selected successfully", "data": {"selected_skills": skill_ids}}, status=status.HTTP_200_OK)

    def update(self, request, user_id=None):
        skill_ids = request.data.get('skill_ids', [])

        if not user_id or not skill_ids:
            return Response({"error": "user_id and skill_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        skills = Skill.objects.filter(id__in=skill_ids)
        if skills.count() != len(skill_ids):
            return Response({"error": "Some skills are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_skills.set(skills)
        profile.save()

        return Response({"status": "success", "message": "Skills updated successfully", "data": {"selected_skills": skill_ids}}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_skills.clear()
        profile.save()

        return Response({"status": "success", "message": "Skills removed successfully"}, status=status.HTTP_200_OK)

class PrimarySkillSelectionView(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        primary_skill_id = request.data.get('primary_skill_id')

        if not user_id or not primary_skill_id:
            return Response({"error": "user_id and primary_skill_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        primary_skill = Skill.objects.filter(id=primary_skill_id).first()
        if not primary_skill or primary_skill not in profile.selected_skills.all():
            return Response({"error": "Primary skill must be chosen from selected skills."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_primary_skill = primary_skill
        profile.save()

        return Response({"status": "success", "message": "Primary skill selected successfully", "data": {"primary_skill": primary_skill.name}}, status=status.HTTP_200_OK)

    def update(self, request, user_id=None):
        primary_skill_id = request.data.get('primary_skill_id')

        if not user_id or not primary_skill_id:
            return Response({"error": "user_id and primary_skill_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        primary_skill = Skill.objects.filter(id=primary_skill_id).first()
        if not primary_skill or primary_skill not in profile.selected_skills.all():
            return Response({"error": "Primary skill must be chosen from selected skills."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_primary_skill = primary_skill
        profile.save()

        return Response({"status": "success", "message": "Primary skill updated successfully", "data": {"primary_skill": primary_skill.name}}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_primary_skill = None
        profile.save()

        return Response({"status": "success", "message": "Primary skill removed successfully"}, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"status": "error", "message": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "user_type": request.data.get('user_type', profile.user_type or "2"),
            "bio": request.data.get('bio', profile.bio),
            "cover_image": request.data.get('cover_image', profile.cover_image),
            "profile_image": request.data.get('profile_image', profile.profile_image),
            "date_of_birth": request.data.get('date_of_birth', profile.date_of_birth),
            "age": request.data.get('age', profile.age),
            "location": request.data.get('location', profile.location),
            "height": request.data.get('height', profile.height),
            "weight": request.data.get('weight', profile.weight),
        }

        serializer = ProfileCreateSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Profile created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Profile creation failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, user_id=None):
        profile = get_profile(user_id)
        
        if not profile:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileCreateSerializer(profile)
        return Response({
            "status": "success",
            "message": "Profile details retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, user_id=None):
        profile = get_profile(user_id)
        
        if not profile:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileCreateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "Profile update failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ExperienceViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is a required parameter."}, status=status.HTTP_400_BAD_REQUEST)

        experiences = Experience.objects.filter(user_id=user_id)
        if not experiences.exists():
            return Response({
                "status": "error",
                "message": "No experiences found for the specified user.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experiences, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ExperienceSerializer(data=request.data)
        
        if not request.data.get('user'):
            return Response({"error": "User ID is required to create experience."}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Experience added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Experience creation failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            experience = Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return Response({"error": "Experience not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Experience updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "Experience update failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            experience = Experience.objects.get(pk=pk)
            experience.delete()
            return Response({
                "status": "success",
                "message": "Experience deleted successfully"
            }, status=status.HTTP_200_OK)
        except Experience.DoesNotExist:
            return Response({"error": "Experience not found."}, status=status.HTTP_404_NOT_FOUND)

class EducationViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is a required parameter."}, status=status.HTTP_400_BAD_REQUEST)

        education = Education.objects.filter(user_id=user_id)
        if not education.exists():
            return Response({
                "status": "error",
                "message": "No education records found for the specified user.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EducationSerializer(data=request.data)

        if not request.data.get('user'):
            return Response({"error": "User ID is required to create education entry."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Education added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Education creation failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            education = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response({"error": "Education record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EducationSerializer(education, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Education record updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "Education update failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            education = Education.objects.get(pk=pk)
            education.delete()
            return Response({
                "status": "success",
                "message": "Education record deleted successfully"
            }, status=status.HTTP_200_OK)
        except Education.DoesNotExist:
            return Response({"error": "Education record not found."}, status=status.HTTP_404_NOT_FOUND)


class DocumentVerificationViewSet(viewsets.ViewSet):

    def verify_aadhar(self, request):
        serializer = AadharVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Aadhar Update Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Aadhar verification failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def verify_passport(self, request):
        serializer = PassportVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Passport Update Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Passport verification failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def verify_dl(self, request):
        serializer = DLVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Driver's License Update Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Driver's License verification failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        

class DocumentUploadView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "File is required."},status=status.HTTP_400_BAD_REQUEST)

        data = {
            "user": user.id,
            "file": file
        }
        serializer = DocumentUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "File uploaded successfully",
                "data": {
                    "status": "Document pending",
                    "file_url": serializer.instance.file.url,
                    "verify_status": 1
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "File upload failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)