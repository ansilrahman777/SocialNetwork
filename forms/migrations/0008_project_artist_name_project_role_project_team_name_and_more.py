# Generated by Django 5.0.3 on 2024-11-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_remove_project_media_files_remove_project_team_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='artist_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='role',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='team_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
