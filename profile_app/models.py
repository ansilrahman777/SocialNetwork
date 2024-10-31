from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('1', 'Admin'),
        ('2', 'Regular User'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_app_profile')
    mobile_or_email = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    selected_industries = models.CharField(max_length=100)  # Comma-separated values
    selected_primary_industry = models.CharField(max_length=10)
    selected_skills = models.CharField(max_length=100)  # Comma-separated values
    selected_primary_skill = models.CharField(max_length=10)
    cover_image = models.ImageField(upload_to='cover_images/', blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    bio = models.TextField()
    date_of_birth = models.DateField()
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=5, decimal_places=1)
    weight = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s profile" if self.user else "UserProfile without user"


class Industry(models.Model):
    name = models.CharField(max_length=255)
    industry_image = models.ImageField(upload_to='industry_images/')  # Ensure MEDIA_URL is set up

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=255)
    skill_image = models.ImageField(upload_to='skill_images/')  # Ensure MEDIA_URL is set up
    industry = models.ForeignKey(Industry, related_name='skills', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AadharVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mobile_or_email = models.CharField(max_length=255)
    aadhar_cn = models.CharField(max_length=12, unique=True)
    aadhar_fname = models.CharField(max_length=255)
    verify_status = models.CharField(max_length=50, default="Document pending")

    def __str__(self):
        return f'{self.aadhar_fname} ({self.aadhar_cn})'



class PassportVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mobile_or_email = models.CharField(max_length=255)
    ps_cn = models.CharField(max_length=12, unique=True)
    ps_fname = models.CharField(max_length=255)
    ps_isscountry = models.CharField(max_length=255)
    ps_dateexp = models.DateField()
    verify_status = models.CharField(max_length=50, default="Document pending")

    def __str__(self):
        return f'{self.ps_fname} ({self.ps_cn})'


class DriverLicenseVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mobile_or_email = models.CharField(max_length=255)
    dl_ln = models.CharField(max_length=15, unique=True)  # Assuming DL number is unique
    dl_fname = models.CharField(max_length=255)
    dl_isscstate = models.CharField(max_length=255)
    verify_status = models.CharField(max_length=50, default="Document pending")

    def __str__(self):
        return f'{self.dl_fname} ({self.dl_ln})'