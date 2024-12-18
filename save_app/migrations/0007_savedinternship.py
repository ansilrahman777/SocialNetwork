# Generated by Django 5.0.3 on 2024-11-14 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0008_project_artist_name_project_role_project_team_name_and_more'),
        ('save_app', '0006_savedevent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedInternship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by', to='forms.internship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_internships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'internship')},
            },
        ),
    ]
