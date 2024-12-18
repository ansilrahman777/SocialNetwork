# Generated by Django 5.0.3 on 2024-10-18 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crea_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnboardingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('short_description', models.TextField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]
