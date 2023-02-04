from django.shortcuts import render, redirect
from .forms import NewUserForm, NewDriverForm, DeleteDriverForm
from .models import Driver
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import DriverSerializer, RideSerializer
from django.contrib.auth.forms import AuthenticationForm



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def create_driver(request):
	if request.method == "POST":
		form = NewDriverForm(request.POST)
		if form.is_valid():
			driver = Driver(user=request.user, phone_num=form.cleaned_data.get("phone_num"), car_type=form.cleaned_data.get("car_type")
				, license_plate=form.cleaned_data.get("license_plate"), max_pass=form.cleaned_data.get("max_pass"), special_info=form.cleaned_data.get("special_info"))
			driver.save()
			messages.success(request, "Successfully added as a driver." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewDriverForm()
	return render (request=request, template_name="registration/register_driver.html", context={"register_driver_form":form})

def delete_driver(request):
	if request.method == "POST":
		print("gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaetting here")
		driver = Driver.objects.get(user=request.user)
		driver.delete()
		return redirect("home")
	form = DeleteDriverForm()
	return render (request=request, template_name="registration/unregister_driver.html", context={"delete_driver_form":form})

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
