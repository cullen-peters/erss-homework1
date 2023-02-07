from django.contrib import admin

from .models import Driver, Ride


class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type', 'max_pass')

class DataAdminRide(admin.ModelAdmin):
    list_display = ('owner', 'driver', 'destination', 'passengers', 'arrival_date', 'arrival_time')

admin.site.register(Ride, DataAdminRide)
admin.site.register(Driver, DriverAdmin)
