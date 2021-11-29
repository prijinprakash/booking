from rest_framework import serializers

from listing.models import BookingInfo


class BookingInfoSerializer(serializers.ModelSerializer):
    listing_type = serializers.SerializerMethodField()
    title = serializers.CharField(source='listing.title')
    country = serializers.CharField(source='listing.country')
    city = serializers.CharField(source='listing.city')

    def get_listing_type(self, obj):
        listing = obj.listing
        return listing.get_choices()[listing.listing_type]

    class Meta:
        model = BookingInfo
        fields = ['listing_type', 'title', 'country', 'city', 'price']
        read_only_fields = ['listing_type', 'title', 'country', 'city', 'price']
