# Generated by Django 5.0.3 on 2024-10-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_alter_internship_user_alter_apprenticeship_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='cancelled_cheque',
            field=models.FileField(upload_to='cheques/'),
        ),
        migrations.AlterField(
            model_name='uploads',
            name='pan_card',
            field=models.FileField(upload_to='pan_cards/'),
        ),
    ]
