# Generated by Django 5.0.3 on 2024-10-28 05:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile_app', '0002_remove_profile_mobile_or_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('1', 'Admin'), ('2', 'Regular User')], default='2', max_length=1),
        ),
        migrations.CreateModel(
            name='AadharVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_cn', models.CharField(max_length=12)),
                ('aadhar_fname', models.CharField(max_length=100)),
                ('mobile_or_email', models.EmailField(max_length=254)),
                ('status', models.CharField(default='Document pending', max_length=20)),
                ('verify_status', models.CharField(default='1', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DLVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dl_ln', models.CharField(max_length=20)),
                ('dl_fname', models.CharField(max_length=100)),
                ('dl_isscstate', models.CharField(max_length=100)),
                ('mobile_or_email', models.EmailField(max_length=254)),
                ('status', models.CharField(default='Verification Completed', max_length=20)),
                ('verify_status', models.CharField(default='3', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PassportVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ps_cn', models.CharField(max_length=15)),
                ('ps_fname', models.CharField(max_length=100)),
                ('ps_isscountry', models.CharField(max_length=100)),
                ('ps_dateexp', models.DateField()),
                ('mobile_or_email', models.EmailField(max_length=254)),
                ('status', models.CharField(default='Document pending', max_length=20)),
                ('verify_status', models.CharField(default='2', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]