# Generated by Django 5.0.3 on 2024-11-03 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0002_rename_created_at_block_blocked_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='reason',
            new_name='reason_details',
        ),
        migrations.AddField(
            model_name='block',
            name='common_reason',
            field=models.CharField(blank=True, choices=[('spam', 'Spam'), ('harassment', 'Harassment'), ('inappropriate', 'Inappropriate Content'), ('other', 'Other')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_reason', models.CharField(blank=True, choices=[('spam', 'Spam'), ('harassment', 'Harassment'), ('fake_profile', 'Fake Profile'), ('inappropriate', 'Inappropriate Content'), ('other', 'Other')], max_length=50, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_users_set', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_by_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]