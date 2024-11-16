from django.db import models
from django.contrib.auth import get_user_model
from crea_app.storages import UthoStorage
from .utils import project_upload_to

CustomUser = get_user_model()

class GigWork(models.Model):
    WORK_TYPE_CHOICES = [
        ('freelance', 'Freelance'),
        ('contract', 'Contract'),
        ('part-time', 'Part-time'),
        ('full-time', 'Full-time'),
    ]

    HOURS_TYPE_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('negotiable', 'Negotiable'),
        ('hourly', 'Hourly'),
    ]

    WORK_METHOD_CHOICES = [
        ('onsite', 'Onsite'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]

    PROMOTION_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('featured', 'Featured'),
    ]
    
    PROGRESS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    project_id = models.CharField(max_length=255)
    gig_title = models.CharField(max_length=255)
    short_description = models.TextField()
    work_hours = models.IntegerField()
    hours_type = models.CharField(max_length=50, choices=HOURS_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=50, choices=PRICE_TYPE_CHOICES)
    skills = models.JSONField()  # Store skills as a list
    progress_of_project = models.CharField(max_length=50 ,choices=PROGRESS_CHOICES)
    work_method = models.CharField(max_length=50, choices=WORK_METHOD_CHOICES)
    promotion = models.CharField(max_length=50, choices=PROMOTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # To track the last update

    def __str__(self):
        return self.gig_title

# Casting Call Model
class CastingCall(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    project_link = models.URLField()
    short_description = models.TextField()
    gender = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    role_type = models.CharField(max_length=50)
    age = models.CharField(max_length=20)
    skills = models.JSONField()  # Store skills as a JSON list
    height = models.CharField(max_length=20)
    body_type = models.CharField(max_length=50)
    script_file = models.FileField(upload_to='scripts/', null=True, blank=True)  # PDF or ZIP
    script_url = models.URLField(null=True, blank=True)
    audition_type = models.CharField(max_length=50)
    offline_location = models.CharField(max_length=255, null=True, blank=True)
    casting_call_date = models.DateField()
    casting_call_end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

# Project Model
class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    project_tagline = models.CharField(max_length=255)
    film_name = models.CharField(max_length=255)
    film_role = models.CharField(max_length=255)
    project_status = models.CharField(max_length=50)
    progress_percentage = models.IntegerField()
    project_type = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    description = models.TextField()
    primary_email = models.EmailField()
    secondary_email = models.EmailField()
    team_name = models.CharField(max_length=255, blank=True, null=True)  # New field for team name
    artist_name = models.CharField(max_length=255, blank=True, null=True)  # New field for artist name
    role = models.CharField(max_length=255, blank=True, null=True)  # New field for role
    
    # Separate fields for image and video uploads
    image_files = models.ImageField(
        storage=UthoStorage(),
        upload_to=project_upload_to,
        blank=True,
        null=True
    )
    video_files = models.FileField(
        storage=UthoStorage(),
        upload_to=project_upload_to,
        blank=True,
        null=True
    )
    hashtags = models.JSONField()  # JSON for hashtags
    press_release_link = models.URLField(null=True, blank=True)
    media_release_link = models.URLField(null=True, blank=True)
    social_media_links = models.JSONField()  # JSON for social media links
    genre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title

class BankDetails(models.Model):
    beneficiary_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.beneficiary_name} - {self.bank_name}"

class Uploads(models.Model):  
    pan_card = models.FileField(upload_to='pan_cards/')  
    cancelled_cheque = models.FileField(upload_to='cheques/')  

    def __str__(self):
        return f"Uploads for {self.pan_card.name}"

class EventDetails(models.Model):
    event_title = models.CharField(max_length=200)
    event_overview = models.TextField()
    event_location = models.CharField(max_length=255)
    event_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.IntegerField()
    event_type = models.CharField(max_length=50)
    event_date = models.DateField()
    event_time = models.TimeField()

    def __str__(self):
        return self.event_title

class EventRegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_registrations')
    organization_name = models.CharField(max_length=100)
    pan_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    gst_status = models.CharField(max_length=3)
    gst_number = models.CharField(max_length=15)
    host_name = models.CharField(max_length=100)
    email = models.EmailField()  # Changed from enter_email_address for clarity
    mobile_number = models.CharField(max_length=15)

    # One-to-One relationships
    bank_details = models.OneToOneField(BankDetails, on_delete=models.CASCADE, related_name='event_registration')
    uploads = models.ForeignKey(Uploads, on_delete=models.CASCADE)
    event_details = models.OneToOneField(EventDetails, on_delete=models.CASCADE, related_name='event_registration')

    def __str__(self):
        return f"{self.organization_name} - {self.event_details.event_title}"
    
class Internship(models.Model):
    USER_METHOD_CHOICES = [
        ('individual', 'Individual'),
        ('organisation', 'Organisation')
    ]

    INTERNSHIP_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('remote', 'Remote'),
    ]

    TYPE_OF_WORK_CHOICES = [
        ('development', 'Development'),
        ('research', 'Research'),
        ('support', 'Support'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='internships')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()  # Changed from enter_email_address for clarity
    mobile_number = models.CharField(max_length=20)
    organisation_name = models.CharField(max_length=100)
    intern_method = models.CharField(max_length=20, choices=USER_METHOD_CHOICES)
    internship_title = models.CharField(max_length=100)
    skills_list = models.JSONField()
    internship_type = models.CharField(max_length=10, choices=INTERNSHIP_TYPE_CHOICES)
    type_of_work = models.CharField(max_length=20, choices=TYPE_OF_WORK_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    job_responsibilities = models.TextField()
    duration = models.IntegerField()  # Hours per week

    def __str__(self):
        return f"{self.internship_title} - {self.organisation_name}"

class Apprenticeship(models.Model):
    USER_METHOD_CHOICES = [
        ('individual', 'Individual'),
        ('organisation', 'Organisation')
    ]

    APPRENTICESHIP_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('remote', 'Remote'),
    ]

    TYPE_OF_WORK_CHOICES = [
        ('development', 'Development'),
        ('research', 'Research'),
        ('support', 'Support'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='apprenticeships')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()  # Changed from enter_email_address for clarity
    mobile_number = models.CharField(max_length=20)
    organisation_name = models.CharField(max_length=100)
    apprenticeship_method = models.CharField(max_length=20, choices=USER_METHOD_CHOICES)
    apprenticeship_title = models.CharField(max_length=100)
    skills_list = models.JSONField()
    apprenticeship_type = models.CharField(max_length=10, choices=APPRENTICESHIP_TYPE_CHOICES)
    type_of_work = models.CharField(max_length=20, choices=TYPE_OF_WORK_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    job_responsibilities = models.TextField()
    duration = models.IntegerField()  # Hours per week

    def __str__(self):
        return f"{self.apprenticeship_title} - {self.organisation_name}"

