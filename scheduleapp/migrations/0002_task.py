# Generated by Django 4.2.17 on 2025-01-03 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executer', models.CharField(max_length=200, null=True)),
                ('startdate', models.CharField(max_length=200, null=True)),
                ('preiod', models.IntegerField(default=0, null=True)),
                ('enddate', models.CharField(max_length=100, null=True)),
                ('finishdate', models.CharField(max_length=100, null=True)),
                ('pariority', models.CharField(max_length=100, null=True)),
                ('task_sub', models.CharField(max_length=100, null=True)),
                ('task_desc', models.TextField(null=True)),
                ('active', models.BooleanField(default=False)),
                ('is_seen', models.BooleanField(default=False)),
            ],
        ),
    ]
