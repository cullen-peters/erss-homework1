from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Ride, CAR_TYPES, DRIVER_CAR_TYPES
from tempus_dominus.widgets import DatePicker, TimePicker

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
	phone_number = forms.CharField(required=True)
	car_type = forms.ChoiceField(choices=DRIVER_CAR_TYPES)
	license_plate = forms.CharField(required=True)
	max_pass = forms.IntegerField(required=True, max_value=20, min_value=1)

	class Meta:
		model = Driver
		fields = ("phone_number", "car_type", "license_plate", "max_pass", "special_info")

	def save(self, commit=True):
		driver = super(NewDriverForm, self).save(commit=False)
		if commit:
			driver.save()
		return driver

class UpdateDriverForm(forms.ModelForm):
	phone_number = forms.CharField(required=True)
	car_type = forms.ChoiceField(choices=DRIVER_CAR_TYPES)
	license_plate = forms.CharField(required=True)
	max_pass = forms.CharField(required=True)
	class Meta:
		model = Driver
		fields = ("phone_number", "car_type", "license_plate", "max_pass", "special_info")

	def save(self, commit=True):
		driver = super(UpdateDriverForm, self).save(commit=False)
		if commit:
			driver.save()
		return driver

class RideRequestForm(forms.ModelForm):
	destination = forms.CharField(required=True)
	arrival_date = forms.DateField(widget=forms.DateInput(
	format=('%Y-%m-%d'),
	attrs={'class': 'form-control', 
			'placeholder': 'Select a date',
			'type': 'date'
			}))
	arrival_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
	passengers = forms.IntegerField(required=True, max_value=20, min_value=1)
	car_type = forms.ChoiceField(choices=CAR_TYPES, required=False)
	special_info = forms.CharField(required=False)
	shared = forms.BooleanField(required=False)
	class Meta:
			model = Ride
			fields = ("destination", "arrival_date", "arrival_time", "passengers", "car_type", "special_info", "shared")
	def save(self, commit=True):
			return

class RideViewForm(forms.ModelForm):
	driver = forms.CharField(disabled=True)
	owner = forms.CharField(disabled=True)
	destination = forms.CharField(disabled=True)
	arrival_date = forms.DateField(disabled=True)
	arrival_time = forms.TimeField(disabled=True)
	passengers = forms.IntegerField(disabled=True, max_value=20, min_value=1)
	car_type = forms.ChoiceField(choices=CAR_TYPES, disabled=True)
	special_info = forms.CharField(disabled=True)
	sharers = forms.ModelMultipleChoiceField(disabled=True, queryset=User.objects)
	shared = forms.BooleanField(disabled=True)
	class Meta:
			model = Ride
			fields = ("driver", "owner", "destination", "arrival_date", "arrival_time", "passengers", "car_type", "special_info", "shared", 'sharers')

	def save(self, commit=True):
		return

class EditRideForm(forms.ModelForm):
        destination = forms.CharField(required=True)
        arrival_date = forms.DateField(widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }))
        arrival_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
        passengers = forms.IntegerField(required=True, max_value=20, min_value=1)
        car_type = forms.ChoiceField(choices=CAR_TYPES, required=False)
        special_info = forms.CharField(required=False)
        shared = forms.BooleanField(required=False)
        class Meta:
                model = Ride
                fields = ("destination", "arrival_date", "arrival_time", "passengers", "car_type", "special_info", "shared")

        def save(self, commit=True):
                ride = super(EditRideForm, self).save(commit=False)
                if commit:
                        ride.save()
                return ride
                
        
class DeleteDriverForm(forms.Form):
	class Meta:
		model = Driver
		fields = ("phone_number", "car_type", "license_plate", "max_pass", "special_info")

class DriverSearchForm(forms.Form):
        min_date = forms.DateField(widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       }), required=False)
        min_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),required=False)
        max_date = forms.DateField(widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       }), required=False)
        max_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
        destination = forms.CharField(required=False)

class SharerSearchForm(forms.Form):
        min_date = forms.DateField(widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       }), required=False)
        min_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),required=False)
        max_date = forms.DateField(widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       }), required=False)
        max_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
        destination = forms.CharField(required=True)
        num_pass = forms.IntegerField(required=True, max_value=20, min_value=1)
