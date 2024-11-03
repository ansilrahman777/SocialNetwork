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
    COMMON_BLOCK_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('other', 'Other')
    ]

    blocker = models.ForeignKey(User, related_name='blocked_users_set', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_by_set', on_delete=models.CASCADE)
    common_reason = models.CharField(max_length=50, choices=COMMON_BLOCK_REASONS, blank=True, null=True)
    reason_details = models.TextField(blank=True, null=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"

class Report(models.Model):
    COMMON_REPORT_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('fake_profile', 'Fake Profile'),
        ('inappropriate', 'Inappropriate Content'),
        ('other', 'Other')
    ]

    reporter = models.ForeignKey(User, related_name='reported_by_set', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='reported_users_set', on_delete=models.CASCADE)
    common_reason = models.CharField(max_length=50, choices=COMMON_REPORT_REASONS, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter} reported {self.reported}"