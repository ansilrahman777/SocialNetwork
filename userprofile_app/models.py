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

    def __str__(self):
        return f"Profile of {self.user.mobile_or_email}"
    

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


