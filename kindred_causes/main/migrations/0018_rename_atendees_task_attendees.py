# Generated by Django 5.1.5 on 2025-04-20 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_task_atendees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='atendees',
            new_name='attendees',
        ),
    ]
