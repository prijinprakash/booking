from django.urls import path, include
from rest_framework import routers

from .views import BookingInfoListView


urlpatterns = [
    path('units/', BookingInfoListView.as_view(), name='units')
]
