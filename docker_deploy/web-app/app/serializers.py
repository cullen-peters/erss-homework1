from rest_framework import serializers
from .models import Driver, Ride


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            
        )