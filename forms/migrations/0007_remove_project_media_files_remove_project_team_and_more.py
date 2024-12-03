# Generated by Django 5.0.3 on 2024-11-09 06:10

import django.db.models.deletion
import posts_app.backblaze_custom_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_alter_gigwork_progress_of_project_delete_postfeed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='media_files',
        ),
        migrations.RemoveField(
            model_name='project',
            name='team',
        ),
        # migrations.AddField(
        #     model_name='project',
        #     name='image_files',
        #     field=models.ImageField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.project_upload_to),
        # ),
        # migrations.AddField(
        #     model_name='project',
        #     name='video_files',
        #     field=models.FileField(blank=True, null=True, storage=posts_app.backblaze_custom_storage.CustomBackblazeStorage(), upload_to=posts_app.backblaze_custom_storage.project_upload_to),
        # ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255)),
                ('artist_user_id', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='forms.project')),
            ],
        ),
    ]