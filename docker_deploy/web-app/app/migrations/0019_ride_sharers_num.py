# Generated by Django 4.1.6 on 2023-02-08 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_rename_phone_num_driver_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='sharers_num',
            field=models.TextField(blank=True, null=True),
        ),
    ]