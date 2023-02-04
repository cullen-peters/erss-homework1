from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from .serializers import DriverSerializer, RideSerializer


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class DriverViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DriverSerializer

    def perform_create(self, serializer):
        return

class RideViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RideSerializer

    def perform_create(self, serializer):
        return
