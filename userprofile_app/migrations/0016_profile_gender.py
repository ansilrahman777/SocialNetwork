# Generated by Django 5.0.3 on 2024-11-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile_app', '0015_alter_unionassociation_member_since'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
