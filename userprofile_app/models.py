from django.db import models
from django.contrib.auth import get_user_model
from posts_app.backblaze_custom_storage import CustomBackblazeStorage, profile_image_upload_to, cover_image_upload_to, document_upload_to
from social_app.models import Follow

User = get_user_model()

class Role(models.Model):
    # role_name - Example: Aspirant, Professional, Business, Technician
    role_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True) 

class Industry(models.Model):
    # name - Example: Film, Media, Music
    name = models.CharField(max_length=255)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class Skill(models.Model):
    # name - Example: Actor , Heroine, Comedian
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255,null=True, blank=True)
    work_type = models.CharField(max_length=50,null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255,null=True, blank=True)
    institution_name = models.CharField(max_length=255,null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution_name}"

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('1', 'Admin'),
        ('2', 'Regular User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='2') 
    selected_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    selected_industries = models.ManyToManyField(Industry, blank=True)
    selected_primary_industry = models.ForeignKey(Industry, related_name='primary_industry', on_delete=models.SET_NULL, null=True, blank=True)
    selected_skills = models.ManyToManyField(Skill, blank=True)
    selected_primary_skill = models.ForeignKey(Skill, related_name='primary_skill', on_delete=models.SET_NULL, null=True, blank=True)
    
    cover_image = models.FileField(
        storage=CustomBackblazeStorage(),
        upload_to=cover_image_upload_to,
        blank=True,
        null=True
    )
    profile_image = models.FileField(
        storage=CustomBackblazeStorage(),
        upload_to=profile_image_upload_to,
        blank=True,
        null=True
    )
    
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.PositiveIntegerField( null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False) 

    def __str__(self): 
        return f"Profile of {self.user.mobile_or_email}"
    
    @property
    def followers_count(self):
        return Follow.objects.filter(following=self.user).count()

    @property
    def following_count(self):
        return Follow.objects.filter(follower=self.user).count()

    def get_status_color(self, percentage):
        if percentage <= 25:
            return "#FF5722"  # Red
        elif percentage <= 50:
            return "#FFC107"  # Yellow
        elif percentage <= 75:
            return "#FF9800"  # Orange
        else:
            return "#4CAF50"  # Green

    def calculate_section_completion(self):
        sections = [
            {"id": "1", "name": "Basic Profile", "weight": 20, "completion": 0},
            {"id": "2", "name": "Experience", "weight": 15, "completion": 0},
            {"id": "3", "name": "Education", "weight": 20, "completion": 0},
            {"id": "4", "name": "Industry", "weight": 10, "completion": 0},
            {"id": "5", "name": "Skillset", "weight": 15, "completion": 0},
            {"id": "6", "name": "Union & Association", "weight": 10, "completion": 0},
            {"id": "7", "name": "Document Upload & Verification", "weight": 10, "completion": 0},
        ]

        total_completion = 0
        pending_updates = []
        verification_status = {
            "Aadhar Verification": "Pending",
            "Passport Verification": "Pending",
            "DL Verification": "Pending"
        }

        # 1. Basic Profile
        if all([self.user_type, self.cover_image, self.profile_image, self.bio, self.date_of_birth, self.location, self.height, self.weight]):
            sections[0]["completion"] = 100
        total_completion += sections[0]["completion"] * (sections[0]["weight"] / 100)

        # 2. Experience
        if Experience.objects.filter(user=self.user).exists():
            sections[1]["completion"] = 100
        total_completion += sections[1]["completion"] * (sections[1]["weight"] / 100)

        # 3. Education
        if Education.objects.filter(user=self.user).exists():
            sections[2]["completion"] = 100
        total_completion += sections[2]["completion"] * (sections[2]["weight"] / 100)

        # 4. Industry
        if self.selected_industries.exists():
            sections[3]["completion"] = 100
        total_completion += sections[3]["completion"] * (sections[3]["weight"] / 100)

        # 5. Skillset
        if self.selected_skills.exists():
            sections[4]["completion"] = 100
        total_completion += sections[4]["completion"] * (sections[4]["weight"] / 100)

        # 6. Union & Association
        if UnionAssociation.objects.filter(user=self.user).exists():
            sections[5]["completion"] = 100
        total_completion += sections[5]["completion"] * (sections[5]["weight"] / 100)

        # 7. Document Upload & Verification
        document_verified = False
        document_upload_verified = False

        # Check individual verification status
        if AadharVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            document_verified = True
            verification_status["Aadhar Verification"] = "Verified"

        if PassportVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            document_verified = True
            verification_status["Passport Verification"] = "Verified"

        if DLVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            document_verified = True
            verification_status["DL Verification"] = "Verified"

        # Check if any document upload is verified
        if DocumentUpload.objects.filter(user=self.user, verify_status=2).exists():  # Assuming status 2 means verified
            document_upload_verified = True

        # Set completion status for document verification if at least one is verified
        if document_verified and document_upload_verified:
            sections[6]["completion"] = 100
        total_completion += sections[6]["completion"] * (sections[6]["weight"] / 100)

        # Add pending section if document verification and upload are incomplete
        if sections[6]["completion"] < 100:
            pending_updates.append({
                "id": sections[6]["id"],
                "name": sections[6]["name"],
                "pendingPercentage": 100 - sections[6]["completion"],
                "statusColor": "#2196F3"  # Blue
            })

        # Format response and assign colors
        for section in sections:
            completion = section["completion"]
            section["completionPercentage"] = completion * (section["weight"] / 100)
            section["statusColor"] = self.get_status_color(completion)

            # Track pending sections
            if completion < 100:
                pending_updates.append({
                    "id": section["id"],
                    "name": section["name"],
                    "pendingPercentage": 100 - completion,
                    "statusColor": "#2196F3"  # Blue
                })

        total_completion_percentage = round(total_completion, 2)
        total_status_color = self.get_status_color(total_completion_percentage)

        return {
            "totalCompletion": {
                "percentage": total_completion_percentage,
                "statusColor": total_status_color
            },
            "sections": sections,
            "pendingUpdates": pending_updates,
            "verificationStatus": verification_status
        }

class ProfileView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    time_viewed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'viewer')
    

class AadharVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar_cn = models.CharField(max_length=12)
    aadhar_fname = models.CharField(max_length=100)
    mobile_or_email = models.EmailField()
    status = models.CharField(max_length=20, default="Document pending")
    verify_status = models.CharField(max_length=2, default="1")

    def __str__(self):
        return f"Aadhar Verification for {self.user}"

class PassportVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ps_cn = models.CharField(max_length=15)
    ps_fname = models.CharField(max_length=100)
    ps_isscountry = models.CharField(max_length=100)
    ps_dateexp = models.DateField()
    mobile_or_email = models.EmailField()
    status = models.CharField(max_length=20, default="Document pending")
    verify_status = models.CharField(max_length=2, default="1")

    def __str__(self):
        return f"Passport Verification for {self.user}"

class DLVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dl_ln = models.CharField(max_length=20)
    dl_fname = models.CharField(max_length=100)
    dl_isscstate = models.CharField(max_length=100)
    mobile_or_email = models.EmailField()
    status = models.CharField(max_length=20, default="Document pending")
    verify_status = models.CharField(max_length=2, default="1")

    def __str__(self):
        return f"DL Verification for {self.user}"
    
class DocumentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        storage=CustomBackblazeStorage(),
        upload_to=document_upload_to,
        blank=True,
        null=True
    )
    upload_status = models.CharField(max_length=50, default="Document pending")
    verify_status = models.IntegerField(default=1)  # 1 = Pending, 2 = Verified, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document uploaded by {self.user.mobile_or_email}"
    
class UnionAssociation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Name of the Union or Association
    member_since = models.DateField()

    def __str__(self):
        return f"{self.name} - Member since {self.member_since}"


