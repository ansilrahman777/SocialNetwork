from django.db import models
from posts_app.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_by')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_posts')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate saves for the same post by the same user

    def __str__(self):
        return f"{self.user.username} saved {self.post}"

