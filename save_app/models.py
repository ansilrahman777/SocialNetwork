from django.db import models
from posts_app.models import Post
from django.contrib.auth import get_user_model
from userprofile_app.models import Profile
from forms.models import GigWork, CastingCall, Project, EventDetails, Internship, Apprenticeship

User = get_user_model()

class SavedArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_artists')
    artist_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist_profile')

    def __str__(self):
        return f"{self.user.username} saved {self.artist_profile.user.username}"

class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_by')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_posts')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post}"

class SavedProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} saved {self.project.project_title}"
    
class SavedGigWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_gigs')
    gig_work = models.ForeignKey(GigWork, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'gig_work')

    def __str__(self):
        return f"{self.user.username} saved {self.gig_work.gig_title}"
    
class SavedCastingCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_casting_calls')
    casting_call = models.ForeignKey(CastingCall, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'casting_call')

    def __str__(self):
        return f"{self.user.username} saved {self.casting_call.job_title}"
    
class SavedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_events')
    event = models.ForeignKey(EventDetails, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} saved {self.event.event_title}"
    
class SavedInternship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_internships')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'internship')

    def __str__(self):
        return f"{self.user.username} saved {self.internship.internship_title}"
    
class SavedApprenticeship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_apprenticeships')
    apprenticeship = models.ForeignKey(Apprenticeship, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'apprenticeship')

    def __str__(self):
        return f"{self.user.username} saved {self.apprenticeship.apprenticeship_title}"
    
    
