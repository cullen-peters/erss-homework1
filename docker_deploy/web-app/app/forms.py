from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Ride


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="driver")
    # phone_num = models.CharField(max_length=16, null=False, default="000-000-0000")
    # car_type = models.PositiveSmallIntegerField(choices=CAR_TYPES, null=False)
    # license_plate = models.TextField()
    # max_pass = models.SmallIntegerField()
    # special_info = models.TextField(null=True, blank=True)
class NewDriverForm(forms.ModelForm):
	# email = forms.UserField(required=True)

	class Meta:
		model = Driver
		fields = ("phone_num", "car_type", "license_plate", "max_pass", "special_info")

	def save(self, commit=True):
		driver = super(NewDriverForm, self).save(commit=False)
		if commit:
			driver.save()
		return driver

class RideRequestForm(forms.ModelForm):
        class Meta:
                model = Ride
                fields = ("destination", "arrival_date", "arrival_time", "passengers", "car_type", "special_info", "shared")

        def save(self, commit=True):
                return
