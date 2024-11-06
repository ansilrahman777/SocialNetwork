# Generated by Django 5.0.3 on 2024-11-06 05:03

import posts_app.backblaze_custom_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile_app', '0008_unionassociation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=models.FileField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.profile_image_upload_to),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.profile_image_upload_to),
        ),
    ]