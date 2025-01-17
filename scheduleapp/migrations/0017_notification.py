# Generated by Django 5.1.4 on 2025-01-15 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0016_taskprogress_notif_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif', models.CharField(max_length=100, null=True)),
                ('exe_code', models.CharField(max_length=200, null=True)),
                ('notif_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
