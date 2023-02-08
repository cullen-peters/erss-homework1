from django.shortcuts import render, redirect
from .forms import NewUserForm, NewDriverForm, DeleteDriverForm, RideRequestForm, UpdateUserForm, UpdateDriverForm, RideViewForm, EditRideForm, DriverSearchForm, SharerSearchForm
from .models import Driver, Ride, CAR_TYPES, DRIVER_CAR_TYPES
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.mail import send_mail


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
	if request.user.is_authenticated:
		if request.method == "POST":
			form = NewDriverForm(request.POST)
			if form.is_valid():
				driver = Driver(user=request.user, phone_number=form.cleaned_data.get("phone_number"), car_type=form.cleaned_data.get("car_type")
					, license_plate=form.cleaned_data.get("license_plate"), max_pass=form.cleaned_data.get("max_pass"), special_info=form.cleaned_data.get("special_info"))
				driver.save()
				messages.success(request, "Successfully added as a driver." )
				return redirect("home")
			messages.error(request, "Unsuccessful registration. Invalid information.")
		form = NewDriverForm()
		return render (request=request, template_name="registration/register_driver.html", context={"register_driver_form":form})
	return redirect("login")

def delete_driver(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			driver = Driver.objects.get(user=request.user)
			driver.delete()
			return redirect("home")
		form = DeleteDriverForm()
		return render (request=request, template_name="registration/unregister_driver.html", context={"delete_driver_form":form})
	return redirect("login")

def update_driver(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = UpdateDriverForm(request.POST, instance=Driver.objects.get(user=request.user))
			if form.is_valid():
				form.save()
				return redirect("home")
		form = UpdateDriverForm(instance=Driver.objects.get(user=request.user))
		print(DRIVER_CAR_TYPES[Driver.objects.get(user=request.user).car_type - 1][1])
		print(Driver.objects.get(user=request.user).car_type)
		return render(request=request, template_name="registration/update_driver.html", context={"update_driver_form":form})
	return redirect("login")

# DRIVER^
# -------------------------------------------------
# RIDES

def ride_request(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = RideRequestForm(request.POST)
			if form.is_valid():
				print(form.cleaned_data)
				print(f'car type: {form.cleaned_data.get("car_type")}')
				ride = Ride(owner=request.user, destination=form.cleaned_data.get("destination"), arrival_date=form.cleaned_data.get("arrival_date"), arrival_time=form.cleaned_data.get("arrival_time"), passengers=form.cleaned_data.get("passengers"), car_type=form.cleaned_data.get("car_type"), special_info=form.cleaned_data.get("special_info"), shared=form.cleaned_data.get("shared"), complete=False)
				ride.save()
				messages.success(request, "Successfully entered ride request.")
				return redirect("ride_list")
			messages.error(request, "Unsuccessful ride request. Invalid information.")
		form = RideRequestForm()
		return render (request=request, template_name="ride_request.html", context={"ride_request_form":form})
	return redirect("login")

def view_ride(request):
	if request.user.is_authenticated:
		if request.method == "POST" and request.META.get('QUERY_STRING', None) is not None:
			ride = Ride.objects.get(pk=request.META.get('QUERY_STRING', None))
			ride.complete = True
			ride.save()
			messages.success(request, "Successfully entered ride request.")
			return redirect("home")
		form = RideViewForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)), initial={'driver': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).driver.__str__, 'owner': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).owner.__str__})
		return render (request=request, template_name="ride_view.html", context={"ride_view_form":form})
	return redirect("login")

def view_ride_without_complete(request):
	if request.user.is_authenticated:
		form = RideViewForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)), initial={'driver': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).driver.__str__, 'owner': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).owner.__str__})
		return render (request=request, template_name="view_single_ride.html", context={"ride_view_form":form})
	return redirect("login")

def view_ride_list(request):
	if request.user.is_authenticated:
		owned_rides = Ride.objects.filter(owner=request.user, driver=None, complete=False)
		shared_rides = Ride.objects.filter(sharers=request.user, driver=None, complete=False)
		confirmed_rides_owned = Ride.objects.exclude(driver__isnull=True).filter(owner=request.user, complete=False)
		confirmed_rides_shared = Ride.objects.exclude(driver__isnull=True).filter(sharers=request.user, complete=False)
		context = {
			'owned_rides': owned_rides,
			'shared_rides': shared_rides,
			'confirmed_rides': confirmed_rides_owned | confirmed_rides_shared,
		}
		return render(request, 'rides.html', context=context)
	return redirect("login")

def edit_ride(request):
        if request.user.is_authenticated:
                if request.method == "POST" and request.META.get('QUERY_STRING', None) is not None:
                        form = EditRideForm(request.POST, instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)))
                        if form.is_valid():
                                form.save()
                                return redirect("ride_list")
                form = EditRideForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)))
                return render(request=request, template_name="edit_ride.html", context={"edit_ride_form":form})
        return redirect("login")

def confirm_ride(request):
	if request.user.is_authenticated:
		if request.method == "POST" and request.META.get('QUERY_STRING', None) is not None:
			ride = Ride.objects.get(pk=request.META.get('QUERY_STRING', None))
			ride.driver = request.user.driver
			ride.save()
			send_list = []
			send_list.append(ride.owner.email)
			if ride.sharers.exists():
				for obj in ride.sharers.all():
					send_list.append(obj.email)
				print(send_list)
			subject = 'Ride Share App Ride Confirmed'
			message = f'Hi! Your ride to {ride.destination} has been confirmed by driver {ride.driver}.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = send_list
			send_mail(subject, message, email_from, recipient_list)

			messages.success(request, "Successfully confirmed ride request.")
			return redirect("home")
		form = RideViewForm(instance=Ride.objects.get(pk=request.META.get('QUERY_STRING', None)), initial={'driver': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).driver.__str__, 'owner': Ride.objects.get(pk=request.META.get('QUERY_STRING', None)).owner.__str__})
		return render (request=request, template_name="confirm_ride.html", context={"ride_view_form":form})
	return redirect("login")

# RIDES ^
# ---------------------------
# SEARCH

def driver_search(request):
	if request.user.is_authenticated:
		open_rides = Ride.objects.filter(complete=False).exclude(owner=request.user).exclude(driver__isnull=False)
		open_rides = open_rides.filter(car_type=0) | open_rides.filter(car_type=request.user.driver.car_type)
		open_rides = open_rides.filter(passengers__lte=request.user.driver.max_pass)
		open_rides = open_rides.filter(special_info="") | open_rides.filter(special_info=None) | open_rides.filter(special_info=request.user.driver.special_info)
		if request.method == "POST":
			form = DriverSearchForm(request.POST)
			if form.is_valid():
				min_date = form.cleaned_data.get("min_date")
				min_time = form.cleaned_data.get("min_time")
				max_date = form.cleaned_data.get("max_date")
				max_time = form.cleaned_data.get("max_time")
				dest = form.cleaned_data.get("destination")
				if min_date:
					print(min_date)
					print(type(min_date))
					open_rides = open_rides.filter(arrival_date__gte=min_date)
				if min_time:
					print(min_time)
					open_rides = open_rides.filter(arrival_time__gte=min_time)
				if max_date:
					print(max_date)
					print(type(max_date))
					open_rides = open_rides.filter(arrival_date__lte=max_date)
				if max_time:
					open_rides = open_rides.filter(arrival_time__lte=max_time)
				if dest:
					open_rides = open_rides.filter(destination=dest)
		else:
			form = DriverSearchForm()
		context = {
			'driver_search_form': form,
			'open_rides': open_rides,
		}
		return render(request=request, template_name="driver_search.html", context=context)
	return redirect("login")

def sharer_search(request):
        if request.user.is_authenticated:
                open_rides = Ride.objects.filter(complete=False, shared=True).exclude(owner=request.user).exclude(driver__isnull=False)
                if request.method == "POST":
                        form = SharerSearchForm(request.POST)
                        if form.is_valid():
                                min_date = form.cleaned_data.get("min_date")
                                min_time = form.cleaned_data.get("min_time")
                                max_date = form.cleaned_data.get("max_date")
                                max_time = form.cleaned_data.get("max_time")
                                dest = form.cleaned_data.get("destination")
                                num_pass = form.cleaned_data.get("num_pass")
                                if min_date:
                                        open_rides = open_rides.filter(arrival_date__gte=min_date)
                                if min_time:
                                        open_rides = open_rides.filter(arrival_time__gte=min_time)
                                if max_date:
                                        open_rides = open_rides.filter(arrival_date__lte=max_date)
                                if dest:
                                        open_rides = open_rides.filter(destination=dest)
                else:
                        form = SharerSearchForm()
                context = {
                        'sharer_search_form': form,
                        'open_rides': open_rides,
                        }
                return render(request=request, template_name="driver_search.html", context=context)
        return redirect("login")
