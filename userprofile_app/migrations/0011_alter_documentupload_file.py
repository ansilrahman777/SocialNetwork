# Generated by Django 5.0.3 on 2024-11-06 07:26

import posts_app.backblaze_custom_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile_app', '0010_alter_profile_cover_image'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='documentupload',
        #     name='file',
        #     field=models.FileField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.document_upload_to),
        # ),
    ]
