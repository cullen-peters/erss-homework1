from django.db import models
from django.contrib.auth.models import User

class Userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="userdata")
