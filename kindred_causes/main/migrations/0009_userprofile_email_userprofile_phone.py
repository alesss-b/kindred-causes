# Generated by Django 5.1.5 on 2025-03-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='john.doe@example.com', max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='(123)-456-7890', max_length=15),
        ),
    ]
