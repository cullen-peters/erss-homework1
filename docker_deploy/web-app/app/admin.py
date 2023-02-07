from django.contrib import admin

from .models import Driver, Ride


class DataAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type')

class DataAdminRide(admin.ModelAdmin):
    list_display = ('owner', 'destination', 'arrival_date', 'arrival_time')

admin.site.register(Ride, DataAdminRide)
admin.site.register(Driver, DataAdmin)
