from django import forms

from .models import BookingInfo, Listing


class CustomListingChoiceField(forms.ModelChoiceField):
    """
    custom field for the listing foreignkey choice field with listing type in label
    for readability in django admin Booking Info form.
    ex: Luxurious Studio (Apartment)
    """

    def label_from_instance(self, listing_obj):
        return f'{listing_obj.title} ({listing_obj.get_choices()[listing_obj.listing_type]})'


class CustomBookingInfoForm(forms.ModelForm):
    """
    custom form for Booking Info in django admin.
    """
    listing = CustomListingChoiceField(queryset=Listing.objects.all())

    class Meta:
        model = BookingInfo
        fields = "__all__"
