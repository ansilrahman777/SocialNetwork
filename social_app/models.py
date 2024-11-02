from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowRequest(models.Model):
    requester = models.ForeignKey(User, related_name='sent_follow_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_follow_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('requester', 'recipient')

    def __str__(self):
        return f"FollowRequest from {self.requester} to {self.recipient} ({self.status})"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocked_users_set', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_by_set', on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"