# Generated by Django 5.0.3 on 2024-11-02 12:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='created_at',
            new_name='blocked_at',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='created_at',
            new_name='followed_at',
        ),
        migrations.AlterField(
            model_name='block',
            name='blocked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='block',
            name='blocker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_follow_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_follow_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
