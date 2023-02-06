from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Ride


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	username = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UpdateUserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	username = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name")

	def clean_data(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')

		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		return email

	def save(self, commit=True):
		user = super(UpdateUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewDriverForm(forms.ModelForm):
	phone_num = forms.CharField(required=True)
	car_type = forms.IntegerField(required=True)
	license_plate = forms.CharField(required=True)
	max_pass = forms.CharField(required=True)

	class Meta:
		model = Driver
		fields = ("phone_num", "car_type", "license_plate", "max_pass", "special_info")

	def save(self, commit=True):
		driver = super(NewDriverForm, self).save(commit=False)
		if commit:
			driver.save()
		return driver

class UpdateDriverForm(forms.ModelForm):
	phone_num = forms.CharField(required=True)
	car_type = forms.IntegerField(required=True, max_value=5, min_value=1)
	license_plate = forms.CharField(required=True)
	max_pass = forms.CharField(required=True)
	class Meta:
		model = Driver
		fields = ("phone_num", "car_type", "license_plate", "max_pass", "special_info")

	def save(self, commit=True):
		driver = super(UpdateDriverForm, self).save(commit=False)
		if commit:
			driver.save()
		return driver

class RideRequestForm(forms.ModelForm):
        class Meta:
                model = Ride
                fields = ("destination", "arrival_date", "arrival_time", "passengers", "car_type", "special_info", "shared")

        def save(self, commit=True):
                return

class DeleteDriverForm(forms.Form):
	class Meta:
		model = Driver
		fields = ("phone_num", "car_type", "license_plate", "max_pass", "special_info")

