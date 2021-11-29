from django.contrib import admin

from .models import *
from .forms import CustomBookingInfoForm


class HotelRoomInline(admin.StackedInline):
    model = HotelRoom
    extra = 0


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_filter = ('listing_type',)
    list_display = ('title', 'listing_type', 'country', 'city')
    search_fields = ['title', 'listing_type', 'country', 'city']


@admin.register(BookingInfo)
class BookingInfoAdmin(admin.ModelAdmin):
    form = CustomBookingInfoForm
    list_filter = ('listing__listing_type',)
    inlines = [HotelRoomInline]
    list_display = ('listing', 'room_type', 'price')
    search_fields = ['listing__title', 'room_type']


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type')
    search_fields = ['room_number', 'room_type__listing__title']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('booking_info', 'check_in_date', 'check_out_date')
