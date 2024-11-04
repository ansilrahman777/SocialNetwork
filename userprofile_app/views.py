import os
import qrcode
from rest_framework.decorators import action
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Profile, ProfileView, Role, Industry, Skill, Experience, Education, UnionAssociation
from .serializers import AadharVerificationSerializer, DLVerificationSerializer, DocumentUploadSerializer, ExperienceSerializer, EducationSerializer, PassportVerificationSerializer, ProfileCompletionStatusSerializer, ProfileCreateSerializer, RoleSerializer, IndustrySerializer, SkillSerializer, UnionAssociationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

def get_profile(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


class RoleListView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        roles = Role.objects.all()
        if not roles.exists():
            return Response({"status": "error", "message": "No roles available"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(roles, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class RoleSelectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [AllowAny]
    
    def list(self, request):
        industries = Industry.objects.all()
        if not industries.exists():
            return Response({"status": "error", "message": "No industries found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = IndustrySerializer(industries, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class IndustrySelectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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

    def list_selected(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        selected_industries = profile.selected_industries.all()
        serializer = IndustrySerializer(selected_industries, many=True)
        
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class PrimaryIndustrySelectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [AllowAny]
    
    def list(self, request):
        skills = Skill.objects.all()
        if not skills.exists():
            return Response({"status": "error", "message": "No skills found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SkillSerializer(skills, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class SkillSelectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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

    # List selected skills for a user
    def list_selected(self, request, user_id=None):
        profile = get_profile(user_id)
        if not profile:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        selected_skills = profile.selected_skills.all()
        if not selected_skills:
            return Response({"status": "error", "message": "No selected skills found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SkillSerializer(selected_skills, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    # Update selected skills for a user
    def update(self, request, user_id=None):
        skill_ids = request.data.get('skill_ids', [])

        if not user_id or not skill_ids:
            return Response({"error": "user_id and skill_ids are required for update."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        skills = Skill.objects.filter(id__in=skill_ids)
        if skills.count() != len(skill_ids):
            return Response({"error": "Some skills are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        profile.selected_skills.set(skills)
        profile.save()

        return Response({"status": "success", "message": "Skills updated successfully", "data": {"selected_skills": skill_ids}}, status=status.HTTP_200_OK)

    # Remove all selected skills for a user
    def destroy(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is required to delete skills."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile(user_id)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.selected_skills.clear()
        profile.save()

        return Response({"status": "success", "message": "All selected skills removed successfully"}, status=status.HTTP_200_OK)

class PrimarySkillSelectionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [IsAuthenticated]
    
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

        viewer = request.user
        if viewer.is_authenticated and viewer.id != profile.user.id:
            # Check if the viewer has already viewed the profile
            if not ProfileView.objects.filter(profile=profile, viewer=viewer).exists():
                ProfileView.objects.create(profile=profile, viewer=viewer)
                profile.view_count += 1
                profile.save()

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
        
    def profile_completion(self, request, user_id=None):
        profile = get_profile(user_id)
        
        if not profile:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        completion_data = profile.calculate_section_completion()
        serializer = ProfileCompletionStatusSerializer(completion_data)
        
        return Response({
            "status": "success",
            "message": "Profile completion status retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['get'], url_path='qr-code')
    def generate_qr_code(self, request, pk=None):
        """
        Generates or retrieves a permanent QR code for the user's profile.
        """
        try:
            profile = Profile.objects.get(user_id=pk)
        except Profile.DoesNotExist:
            return Response({"status": "error", "message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Define the deep link URL for the user's profile
        profile_url = f"myapp://profile/{profile.user_id}/"  # Use your app's custom scheme or frontend URL

        # Define file path and name
        qr_code_filename = f"user_{profile.user_id}_qr.png"
        file_path = os.path.join(settings.MEDIA_ROOT, "qrcodes", qr_code_filename)

        # Check if QR code file already exists, otherwise create it
        if not os.path.exists(file_path):
            qr_code_image = qrcode.make(profile_url)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            qr_code_image.save(file_path)

        # Retrieve the QR code URL
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "qrcodes"))
        qr_code_url = fs.url(qr_code_filename)

        return Response({
            "status": "success",
            "user_id": profile.user_id,
            "qr_code_url": request.build_absolute_uri(qr_code_url)
        }, status=status.HTTP_200_OK)

class ExperienceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
        
class UnionAssociationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request, user_id=None):
        if not user_id:
            return Response({"error": "user_id is a required parameter."}, status=status.HTTP_400_BAD_REQUEST)

        unions = UnionAssociation.objects.filter(user_id=user_id)
        if not unions.exists():
            return Response({
                "status": "error",
                "message": "No union or association records found for the specified user.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UnionAssociationSerializer(unions, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UnionAssociationSerializer(data=request.data)
        
        if not request.data.get('user'):
            return Response({"error": "User ID is required to create union/association entry."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Union/Association added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Union/Association creation failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            union = UnionAssociation.objects.get(pk=pk)
        except UnionAssociation.DoesNotExist:
            return Response({"error": "Union/Association not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnionAssociationSerializer(union, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Union/Association updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "Union/Association update failed due to invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            union = UnionAssociation.objects.get(pk=pk)
            union.delete()
            return Response({
                "status": "success",
                "message": "Union/Association deleted successfully"
            }, status=status.HTTP_200_OK)
        except UnionAssociation.DoesNotExist:
            return Response({"error": "Union/Association not found."}, status=status.HTTP_404_NOT_FOUND)