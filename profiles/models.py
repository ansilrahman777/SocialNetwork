from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('1', 'Admin'),
        ('2', 'Regular User'),
        # Add more user types as needed
    ]

    user_id = models.CharField(max_length=100, primary_key=True)
    mobile_or_email = models.CharField(max_length=100)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    selected_industries = models.CharField(max_length=100)  # Comma-separated values
    selected_primary_industry = models.CharField(max_length=10)
    selected_skills = models.CharField(max_length=100)  # Comma-separated values
    selected_primary_skill = models.CharField(max_length=10)
    cover_image = models.ImageField(upload_to='cover_images/',blank=True)
    profile_image = models.ImageField(upload_to='profile_images/',blank=True)
    bio = models.TextField()
    date_of_birth = models.DateField()
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=5, decimal_places=1)
    weight = models.CharField(max_length=10)

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