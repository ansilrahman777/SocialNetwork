# Generated by Django 5.0.3 on 2024-10-25 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile_or_email',
        ),
    ]
