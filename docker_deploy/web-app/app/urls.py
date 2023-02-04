from django.conf.urls import include
from django.urls import path
from . import views
from .views import DriverViewSet, RideViewSet
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
    # path("", views.homepage, name="homepage"),
    path("login", views.login_request, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
]

