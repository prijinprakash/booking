from django.urls import path

from .views import BookingInfoListView


urlpatterns = [
    path('units/', BookingInfoListView.as_view(), name='units')
]
