from datetime import datetime

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
# from django.db import connection

from listing.models import BookingInfo, Listing
from .serializers import BookingInfoSerializer


class BookingInfoListView(generics.ListAPIView):
    model = BookingInfo
    serializer_class = BookingInfoSerializer

    def get_queryset(self):
        queryset = BookingInfo.objects.all().order_by('price')
        max_price = self.request.query_params.get('max_price', None)
        if max_price is not None:
            try:
                max_price = int(max_price)
            except ValueError:
                return []
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        start_date = request.query_params.get('check_in', None)
        end_date = request.query_params.get('check_out', None)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date is not None else start_date
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date is not None else end_date
        except (TypeError, ValueError):
            return Response('Invalid date format.It should be of the form `YYYY-MM-DD`')

        if start_date and end_date and end_date < start_date:
            return Response('Checkout date can not be less than check in date')

        if start_date is not None or end_date is not None:
            queryset = queryset.select_related('listing').prefetch_related('hotel_rooms')
            available_bookings = []
            for obj in queryset:
                if self.can_make_reservation(start_date, end_date, obj):
                    available_bookings.append(obj.id)
            if available_bookings:
                queryset = queryset.filter(id__in=available_bookings)

        serializer = BookingInfoSerializer(queryset, many=True)
        # print(len(connection.queries))
        return Response({"items": serializer.data})

    @staticmethod
    def can_make_reservation(start_date, end_date, booking_info_obj):
        reservations = booking_info_obj.reservations.all()
        if start_date and end_date:
            query = Q(check_in_date__range=(start_date, end_date)) | \
                    Q(check_out_date__range=(start_date, end_date))
            reservations = reservations.filter(query)
        elif start_date:
            reservations = reservations.filter(check_in_date__lte=start_date, check_out_date__gte=start_date)
        elif end_date:
            reservations = reservations.filter(check_in_date__lte=end_date, check_out_date__gte=end_date)

        if booking_info_obj.listing.listing_type == Listing.HOTEL:
            # atleast one hotel room must be available in the date range
            no_of_hotel_rooms_in_this_booking = len(booking_info_obj.hotel_rooms.all())
            if len(reservations) < no_of_hotel_rooms_in_this_booking:
                return True
            return False
        elif not reservations.exists():
            # no reservations available for the apartment in the date range
            return True

        return False
