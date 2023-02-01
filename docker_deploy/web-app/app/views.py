from django.shortcuts import render
from django.http import HttpResponse
# from djoser.views import UserViewSet


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# class AccountViewSet(UserViewSet):

#     def perform_create(self, serializer):
#         return