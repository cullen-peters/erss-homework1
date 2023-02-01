from django.conf.urls import include
from django.urls import path
from . import views
# from app.views import AccountViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'^users', AccountViewSet)

# accounts_urlpatterns = [
#     # url(r'^api/v1/', include('djoser.urls')),
#     # path(r'^api/v1/', include('djoser.urls.authtoken')),
#     path(r'^api/v1/', include(router.urls))
# ]


urlpatterns = [
    path('', views.index, name='index'),
]