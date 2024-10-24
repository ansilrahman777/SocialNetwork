from django.db import models
from django.contrib.auth import get_user_model
from crea_app.backblaze_storage import BackblazeStorage
import re
from django.utils.text import slugify


CustomUser = get_user_model()

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('1', 'Admin'),
        ('2', 'Regular User'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    selected_industries = models.TextField()
    selected_primary_industry = models.CharField(max_length=100)
    selected_skills = models.TextField()
    selected_primary_skill = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='cover_images/', storage=BackblazeStorage(), blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', storage=BackblazeStorage(), blank=True)
    bio = models.TextField()
    date_of_birth = models.DateField()
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=5, decimal_places=1)
    weight = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def clean_file_name(self, file_name):
        # Remove backslashes and replace with underscores or any preferred character
        sanitized_name = re.sub(r'\\+', '_', file_name)  # Replace backslashes with underscores
        sanitized_name = slugify(sanitized_name)  # This will ensure the name is safe for storage
        return sanitized_name

    def save(self, *args, **kwargs):
        if self.cover_image:
            self.cover_image.name = self.clean_file_name(self.cover_image.name)
        if self.profile_image:
            self.profile_image.name = self.clean_file_name(self.profile_image.name)
        super().save(*args, **kwargs)

class Industry(models.Model):
    name = models.CharField(max_length=255)
    industry_image = models.ImageField(upload_to='industry_images/', storage=BackblazeStorage())

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=255)
    skill_image = models.ImageField(upload_to='skill_images/', storage=BackblazeStorage())
    industry = models.ForeignKey(Industry, related_name='skills', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
