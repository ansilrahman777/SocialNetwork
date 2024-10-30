from django.db import models
from django.contrib.auth import get_user_model

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
    cover_image = models.URLField(null=True, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"Profile of {self.user.mobile_or_email}"

    def calculate_completion_percentage(self):
        total_sections = 9  # Total sections to complete for full verification
        completed_sections = 0
        pending_items = []

        # Check if basic profile details are filled
        if all([self.user_type, self.cover_image, self.profile_image, self.bio,
                self.date_of_birth, self.location, self.height, self.weight]):
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Basic Profile Details",
                "description": "Fill out all basic profile fields like bio, date of birth, height, weight, etc."
            })

        # Check if role is selected
        if self.selected_role:
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Role Selection",
                "description": "Select a role in your profile."
            })

        # Check if at least one industry and one skill are selected
        if self.selected_industries.exists() and self.selected_skills.exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Industry and Skill Selection",
                "description": "Select at least one industry and one skill."
            })

        # Check if education and experience are provided
        if Education.objects.filter(user=self.user).exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Education Entry",
                "description": "Add at least one education entry."
            })
            
        if Experience.objects.filter(user=self.user).exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Experience Entry",
                "description": "Add at least one experience entry."
            })

        # Check if verifications are completed
        if AadharVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Aadhar Verification",
                "description": "Complete Aadhar verification."
            })

        if PassportVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Passport Verification",
                "description": "Complete passport verification."
            })

        if DLVerification.objects.filter(user=self.user, status="Verification Completed").exists():
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Driving License Verification",
                "description": "Complete driving license verification."
            })

        # Check if at least one document is uploaded
        if DocumentUpload.objects.filter(user=self.user, verify_status=2).exists():  # Assuming status 2 means verified
            completed_sections += 1
        else:
            pending_items.append({
                "section": "Document Upload",
                "description": "Upload at least one verified document."
            })

        # Calculate the percentage and round to 2 decimal places
        completion_percentage = round((completed_sections / total_sections) * 100, 2)

        # Update verification status based on completion
        self.is_verified = completion_percentage == 100
        self.save()  # Save the updated verification status

        return completion_percentage, pending_items

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
    verify_status = models.CharField(max_length=2, default="2")

    def __str__(self):
        return f"Passport Verification for {self.user}"

class DLVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dl_ln = models.CharField(max_length=20)
    dl_fname = models.CharField(max_length=100)
    dl_isscstate = models.CharField(max_length=100)
    mobile_or_email = models.EmailField()
    status = models.CharField(max_length=20, default="Verification Completed")
    verify_status = models.CharField(max_length=2, default="3")

    def __str__(self):
        return f"DL Verification for {self.user}"
    
class DocumentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/documents/')
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


