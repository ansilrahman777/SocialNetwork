from django.db import models
from django.conf import settings
from django.utils import timezone
from mimetypes import guess_type

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    media = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        mime_type, _ = guess_type(self.media.name)
        if mime_type:
            if mime_type.startswith('image'):
                self.media_type = 'image'
            elif mime_type.startswith('video'):
                self.media_type = 'video'
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
