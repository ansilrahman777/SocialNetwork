# Generated by Django 5.0.3 on 2024-11-06 05:03

import posts_app.backblaze_custom_storage
import posts_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0002_headshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headshot',
            name='banner',
            field=models.ImageField(storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.headshot_upload_to, validators=[posts_app.models.validate_media_type]),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.post_video_upload_to, validators=[posts_app.models.validate_media_type]),
        ),
    ]
