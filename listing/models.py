from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q


class Listing(models.Model):
    HOTEL = 0
    APARTMENT = 1
    LISTING_TYPE_CHOICES = (
        (HOTEL, 'Hotel'),
        (APARTMENT, 'Apartment'),
    )

    listing_type = models.IntegerField(
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)

    def __str__(self):
        return self.title

    def get_choices(self):
        return dict(self.LISTING_TYPE_CHOICES)


class BookingInfo(models.Model):
    room_type = models.CharField(max_length=255, default='Apartment')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        listing_type = self.listing.listing_type
        if listing_type == Listing.APARTMENT:
            queryset = BookingInfo.objects.filter(listing=self.listing)
            if self.id:
                queryset = queryset.exclude(id=self.id)
            if queryset.exists():
                raise ValidationError(f'Booking Info already exists for the Apartment - {self.listing}')

    def __str__(self):
        return f'{self.listing} - {self.room_type} at {self.price}'

    class Meta:
        verbose_name = "Booking Information"
        verbose_name_plural = "Booking Informations"


class HotelRoom(models.Model):
    room_number = models.CharField(max_length=255)
    room_type = models.ForeignKey(BookingInfo, on_delete=models.CASCADE, related_name="hotel_rooms")

    def __str__(self):
        return self.room_number


class Reservation(models.Model):
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_info = models.ForeignKey(BookingInfo, on_delete=models.CASCADE, related_name="reservations")

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.check_out_date < self.check_in_date:
            raise ValidationError('Checkout date can not be a date before check in date!')
        query = Q(check_in_date__range=(self.check_in_date, self.check_out_date)) | \
                Q(check_out_date__range=(self.check_in_date, self.check_out_date))

        listing_type = self.booking_info.listing.listing_type
        reservations = Reservation.objects.filter(query, booking_info=self.booking_info)
        if self.id:
            reservations = reservations.exclude(id=self.id)
        if listing_type == Listing.APARTMENT and reservations.exists():
            raise ValidationError('Reservation already exists for the apartment between selected dates')
        elif listing_type == Listing.HOTEL:
            # check if atleast one hotel room is available in the date range
            no_of_reservations_in_these_dates = len(reservations)
            no_of_hotel_rooms_in_this_booking = len(HotelRoom.objects.filter(room_type=self.booking_info))
            if no_of_reservations_in_these_dates + 1 > no_of_hotel_rooms_in_this_booking:
                raise ValidationError('No hotel rooms available in the selected room type and dates')