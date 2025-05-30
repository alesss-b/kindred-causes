# Generated by Django 5.1.5 on 2025-04-22 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_notification_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='A detailed description of the Event.', max_length=254, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(help_text='A detailed description of the Skill.', max_length=254, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(help_text='The description of the task.', max_length=254, verbose_name='Description'),
        ),
    ]
