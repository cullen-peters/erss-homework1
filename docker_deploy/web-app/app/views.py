from django.shortcuts import render, redirect
from .forms import NewUserForm, NewDriverForm, DeleteDriverForm, RideRequestForm, UpdateUserForm, UpdateDriverForm, RideViewForm
from .models import Driver, Ride
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


def homepage(request):
	if request.user.is_authenticated:
		if Driver.objects.filter(user=request.user).exists():
			confirmed_rides = Ride.objects.filter(driver=Driver.objects.get(user=request.user), complete=False)
			context = {'confirmed_rides': confirmed_rides}
			return render(request, 'home.html', context=context)
		return render(request, 'home.html')
	return redirect("login")

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
    return redirect("/app/login")

# LOGIN^
# -----------------------------------------------------------------------------------------------------
# USER STUFF

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

def update_user(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = UpdateUserForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect("home")
		form = UpdateUserForm(instance=request.user)
		return render(request=request, template_name="registration/update_user.html", context={"update_user_form":form})
	return redirect("login")

# USER STUFF^
#------------------------------------------------------
# DRIVER

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
		driver = Driver.objects.get(user=request.user)
		driver.delete()
		return redirect("home")
	form = DeleteDriverForm()
	return render (request=request, template_name="registration/unregister_driver.html", context={"delete_driver_form":form})

def update_driver(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = UpdateDriverForm(request.POST, instance=Driver.objects.get(user=request.user))
			if form.is_valid():
				form.save()
				return redirect("home")
		form = UpdateDriverForm(instance=Driver.objects.get(user=request.user))
		return render(request=request, template_name="registration/update_driver.html", context={"update_driver_form":form})
	return redirect("login")

# DRIVER^
# -------------------------------------------------
# RIDES

def ride_request(request):
	if request.method == "POST":
		form = RideRequestForm(request.POST)
		if form.is_valid():
				print("the form is valid")
				ride = Ride(owner=request.user, destination=form.cleaned_data.get("destination"), arrival_date=form.cleaned_data.get("arrival_date"), arrival_time=form.cleaned_data.get("arrival_time"), passengers=form.cleaned_data.get("passengers"), car_type=form.cleaned_data.get("car type"), special_info=form.cleaned_data.get("special_info"), shared=form.cleaned_data.get("shared"), complete=False)
				ride.save()
				messages.success(request, "Successfully entered ride request.")
				return redirect("home")
		messages.error(request, "Unsuccessful ride request. Invalid information.")
	form = RideRequestForm()
	return render (request=request, template_name="ride_request.html", context={"ride_request_form":form})

def view_ride(request):
	if request.user.is_authenticated:
		if request.method == "POST" and request.META.get('QUERY_STRING', None) is not None:
			ride = Ride.objects.get(pk=request.META.get('QUERY_STRING', None))
			ride.complete = True
			ride.save()
			messages.success(request, "Successfully entered ride request.")
			return redirect("home")
		# form = RideViewForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None))).to_representation(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)))
		form = RideViewForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)))
		return render (request=request, template_name="ride_view.html", context={"ride_view_form":form})
	return redirect("login")

def view_ride_list(request):
	if request.user.is_authenticated:
		owned_rides = Ride.objects.filter(owner=request.user, complete=False)
		shared_rides = Ride.objects.filter()
		context = {
			'owned_rides': owned_rides,
			}
		return render(request, 'rides.html', context=context)
	return redirect("login")

