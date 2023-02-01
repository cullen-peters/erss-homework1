from django.contrib import admin

from .models import Driver


class DataAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type')


admin.site.register(Driver, DataAdmin)
