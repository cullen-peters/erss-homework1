from django.contrib import admin

from .models import Driver, UserData


class DataAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Driver, DataAdmin)
admin.site.register(UserData, UserDataAdmin)
