# Generated by Django 4.1.6 on 2023-02-07 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_alter_driver_car_type_alter_ride_car_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='sharers',
            field=models.ManyToManyField(blank=True, related_name='sharers', to=settings.AUTH_USER_MODEL),
        ),
    ]
