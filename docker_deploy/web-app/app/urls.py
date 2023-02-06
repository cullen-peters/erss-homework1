from django.conf.urls import include
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register(r'^users', DriverViewSet)
#router.register(r'^rides', RideViewSet)

# router = DefaultRouter()
# router.register(r'^users', DriverViewSet)

# accounts_urlpatterns = [
#     # url(r'^api/v1/', include('djoser.urls')),
#     # path(r'^api/v1/', include('djoser.urls.authtoken')),
#     path(r'^api/v1/', include(router.urls))
# ]


urlpatterns = [
    path("login", views.login_request, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("register_driver", views.create_driver, name="register_driver"),
    path("ride_request", views.ride_request, name="ride_request"),
    path("unregister_driver", views.delete_driver, name="unregister_driver"),
    path("update_user", views.update_user, name="update_user"),
    path("update_driver", views.update_driver, name="update_driver"),
    path("ride", views.view_ride, name="ride"),
    path("rides", views.view_ride_list, name='ride_list'),
]

