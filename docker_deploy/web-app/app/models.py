from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


CAR_TYPES = (
        (1, 'Sudan'),
        (2, 'Truck'),
        (3, 'Minivan'),
        (4, 'SUV'),
        (5, 'Camper'),
    )
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="driver")
    phone_num = models.CharField(max_length=16, null=False, default="000-000-0000")
    car_type = models.PositiveSmallIntegerField(choices=CAR_TYPES, null=False)
    license_plate = models.CharField(max_length=10)
    max_pass = models.SmallIntegerField()
    special_info = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="userdata")
    # rides = models.ManyToManyField(Ride, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Ride(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride')
    destination = models.TextField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    passengers = models.SmallIntegerField()
    car_type = models.PositiveSmallIntegerField(choices=CAR_TYPES, null=True, blank=True)
    special_info = models.TextField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    complete = models.BooleanField()
    sharers = models.ManyToManyField(UserData, blank=True)


@receiver(post_save, sender=User)
def create_userdata(sender, instance, created, **kwargs):
    if created:
        UserData.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userdata.save()



