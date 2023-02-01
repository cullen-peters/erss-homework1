from django.db import models
from django.contrib.auth.models import User


CAR_TYPES = (
        (1, 'Sudan'),
        (2, 'Truck'),
        (3, 'Minivan'),
        (4, 'SUV'),
    )
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="userdata")
    name = models.TextField()
    car_type = models.PositiveSmallIntegerField(choices=CAR_TYPES, null=False)
    license_plate = models.TextField()
    max_pass = models.SmallIntegerField()
    special_info = models.TextField(null=True, blank=True)

class Ride(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ride')
    destination = models.TextField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    passengers = models.SmallIntegerField()
    car_type = models.PositiveSmallIntegerField(choices=CAR_TYPES, null=True, blank=True)
    special_info = models.TextField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    confirmed = models.BooleanField()
    complete = models.BooleanField()



