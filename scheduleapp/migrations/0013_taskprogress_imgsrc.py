# Generated by Django 4.2.17 on 2025-01-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0012_taskprogress_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskprogress',
            name='imgsrc',
            field=models.TextField(null=True),
        ),
    ]
