# Generated by Django 5.0.3 on 2024-11-08 04:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save_app', '0001_initial'),
        ('userprofile_app', '0011_alter_documentupload_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedArtist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('artist_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by', to='userprofile_app.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_artists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'artist_profile')},
            },
        ),
    ]
