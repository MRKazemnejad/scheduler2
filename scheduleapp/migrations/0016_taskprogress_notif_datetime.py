# Generated by Django 5.1.4 on 2025-01-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0015_remove_image_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskprogress',
            name='notif_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
