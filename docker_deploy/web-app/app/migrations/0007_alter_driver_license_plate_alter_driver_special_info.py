# Generated by Django 4.1.6 on 2023-02-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_userdata_rides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='license_plate',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='driver',
            name='special_info',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
