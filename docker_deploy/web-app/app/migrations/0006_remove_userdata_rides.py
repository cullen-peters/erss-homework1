# Generated by Django 4.1.6 on 2023-02-04 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userdata_rides'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='rides',
        ),
    ]
