from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver


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

class DeleteDriverForm(forms.Form):
	class Meta:
		model = Driver
		fields = ("phone_num", "car_type", "license_plate", "max_pass", "special_info")