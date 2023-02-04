from django.contrib import admin

from .models import Driver, Ride, UserData
from .models import Driver, UserData


class DataAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type')

class DataAdminRide(admin.ModelAdmin):
    list_display = ('owner', 'destination', 'arrival_date', 'arrival_time')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Ride, DataAdminRide)
admin.site.register(Driver, DataAdmin)
admin.site.register(UserData, UserDataAdmin)
