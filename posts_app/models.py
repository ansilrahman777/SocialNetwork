from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from mimetypes import guess_type
# from .backblaze_custom_storage import CustomBackblazeStorage,  post_image_upload_to, post_video_upload_to, headshot_upload_to
from crea_app.storages import UthoStorage
from .utils import headshot_upload_to, post_image_upload_to, post_video_upload_to

User = get_user_model()

def validate_media_type(file):
    mime_type, _ = guess_type(file.name)
    if mime_type:
        if not (mime_type.startswith('image') or mime_type.startswith('video')):
            raise ValidationError("Only image or video files are allowed.")
    else:
        raise ValidationError("Cannot determine the file type. Only images and videos are allowed.")

class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    media = models.FileField(
        storage=UthoStorage(),
        upload_to=post_image_upload_to,
        validators=[validate_media_type],
        blank=True,
        null=True
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.media:
            raise ValidationError("A media file (image or video) is required.")
        
        mime_type, _ = guess_type(self.media.name)
        if mime_type:
            if mime_type.startswith('image'):
                self.media_type = 'image'
                self.media.field.upload_to = post_image_upload_to
            elif mime_type.startswith('video'):
                self.media_type = 'video'
                self.media.field.upload_to = post_video_upload_to
            else:
                raise ValidationError("Only image or video files are allowed.")
        else:
            raise ValidationError("Cannot determine the file type. Only images and videos are allowed.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class Headshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='headshots')
    banner = models.ImageField(
        storage=UthoStorage(),
        upload_to=headshot_upload_to,
        validators=[validate_media_type]
    )
    film_name = models.CharField(max_length=255)
    role_played = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.film_name} - {self.role_played} ({self.user.username})"
