# Generated by Django 4.2.17 on 2025-01-09 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0011_taskprogress_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskprogress',
            name='attachment',
            field=models.BooleanField(default=False),
        ),
    ]
